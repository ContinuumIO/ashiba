import re
import sys
import copy
import json
import time
import shutil
import urllib2
import tempfile
import os, os.path
import multiprocessing as mp
from contextlib import closing, contextmanager
import webbrowser

import ashiba, ashiba.utils

ASHIBA_SHARE = os.path.join(os.path.dirname(__file__), 'share')
print 'ASHIBA_SHARE:', ASHIBA_SHARE

@contextmanager
def stay():
    oldpath = sys.path
    oldcwd = os.getcwd()
    yield
    os.chdir(oldcwd)
    sys.path = oldpath

def stay_put(fcn):
    def decorated_fcn(*args, **kwargs):
        with stay():
            return fcn(*args, **kwargs)
    return decorated_fcn


def get_mtimes(path):
    mtimes = {}
    for root, dirs, files in os.walk(path):
        if os.path.join(path, 'app') not in root:
            for fname in files:
                if not (fname.startswith('.') or fname.endswith('.pyc')):
                    fpath = os.path.join(root, fname)
                    mtimes[fpath] = os.path.getmtime(fpath)
    return mtimes

def templatify_html(in_file):
    if isinstance(in_file, file):
        buf = in_file.read()
    else:
        buf = in_file

    for search_str in ['{% block content %}',
                       '{% extends "app_template.html" %}']:
        if search_str not in buf:
            buf = search_str + '\n' + buf

    search_str = '{% endblock content %}'
    if search_str not in buf:
        buf += '\n' + search_str

    return buf

@stay_put
def _compile(args):
    path = args.path
    os.chdir(path)
    if os.getcwd() not in sys.path:
        sys.path.insert(0, os.getcwd())

    import settings
    SETTINGS = {k:v for k,v in vars(settings).items() \
                        if not k.startswith('__')}
    import handlers

    if os.path.isfile('app'):
        sys.exit("Fatal: \
            There can't be a file named 'app' in the project dir.")
    elif os.path.isdir('app'):
        shutil.rmtree('app')
    shutil.copytree(
        os.path.join(ASHIBA_SHARE, 'compiled_project_files'), 'app')

    ENAML = False
    if os.path.isfile('myapp.enaml'):
        compile_enaml('myapp.enaml')
        ENAML = True

    for fname in [x for x in os.listdir('.') if not x.startswith('.')]:
        root, ext = os.path.splitext(fname)
        if ext in ['.py']:
            shutil.copy(fname, os.path.join('app', fname))
        elif ext == '.html':
            if root != 'myapp':
                shutil.copy(fname, os.path.join('app', 'templates', fname))
            elif not ENAML:
                in_file = open(fname)
                out_file = open(os.path.join('app', 'templates', fname), 'w')
                out_file.write(templatify_html(in_file))
                out_file.close()

    if os.path.isdir('static'):
        for item in [os.path.join('static', x) for x in os.listdir('static')]:
            src, dst = item, os.path.join('app', item)
            if os.path.isdir(item):
                shutil.copytree(src, dst)
            else:
                shutil.copy(src, dst)

    for item in SETTINGS.get('DATA_FILES', []):
        src, dst = item, os.path.join('app', item)
        try:
            shutil.copy(src, dst)
        except IOError:
            print 'Error copying "{}".'.format(item)
        else:
            print 'Copied data file:', item

    file_path = os.path.join('app','static','ashiba_compiled.js')
    print "Writing to:", os.path.abspath(file_path)
    outfile = open(file_path, 'w')
    outfile.write("/* Compiled with Ashiba v{} */\n".format(ashiba.__version__))
    outfile.write("\n$(window).load(function(){")
    fcn_names = [k for k in vars(handlers) if re.match('[\\w]+?__[\\w]+', k)]

    for fcn_name in fcn_names:
        print "--> Translating", fcn_name
        name, event = fcn_name.rsplit('__', 1)
        if name.startswith('_'):
            selector = '.'
        else:
            selector = '#'
        jquery_string = """
  $("{selector}{name}").on("{event}",
    ashiba.eventHandlerFactory("{name}", "{event}")
  );""".format(selector=selector, name=name.lstrip('_'), event=event)

        outfile.write(jquery_string)

    outfile.write("\n});") #end document.ready
    outfile.close()

def _init(args):
    path = args.path
    print "Init:", path
    if os.path.exists(path):
        sys.exit("Fatal: Path '{}' already exists.".format(
            os.path.abspath(path)))
    shutil.copytree(os.path.join(ASHIBA_SHARE, 'new_project_files'), path)

def _clean(args):
    for path in args.paths:
        if os.path.isdir(path):
            clean_app_dir(path)
        else:
            print '"{}" is not a directory. Skipping.'.format(path)

def clean_app_dir(path):
    for app_dir in [os.path.join(path, d) for d in ['app', 'build']]:
        if os.path.isdir(app_dir):
            print "CLEAN: {}".format(app_dir)
            shutil.rmtree(app_dir)

    modified = os.path.join(path, '.modified.json')
    if os.path.isfile(modified):
        os.remove(modified)

    for root, dirs, files in os.walk(path):
        for fname in files:
            if fname.endswith('.pyc'):
                os.remove(os.path.join(root, fname))

def compile_check(args):
    path = args.path
    app_path = os.path.abspath(os.path.join(path, 'app'))

    mtimes = get_mtimes(path)
    mtime_fname = os.path.abspath(os.path.join(path, '.modified.json'))
    try:
        old_mtimes = json.load(open(mtime_fname))
    except (IOError, ValueError):
        old_mtimes = {}
    if (not os.path.isdir(app_path)
            or mtimes != old_mtimes
            or vars(args).get('recompile')):
        print "--- RECOMPILING before start ---"
        _compile(args)
        mtimes = get_mtimes(path)

    with closing(open(mtime_fname, 'w')) as mtime_file:
        json.dump(mtimes, mtime_file)

def _start(args):
    path = args.path
    app_path = os.path.abspath(os.path.join(path, 'app'))

    compile_check(args)

    print "APP_PATH:", app_path
    sys.path.insert(0, app_path)
    os.chdir(app_path)

    initial_port = args.port
    host, port = 'localhost', ashiba.utils.get_port('localhost', initial_port)
    if vars(args).get('open_browser'):
        url = "http://{}:{}/".format(host, port)
        webbrowser.open_new(url)

    import flask_loader
    flask_loader.app.run(host=host, port=port,
                         debug       =True,
                         threaded    =True,
                         use_reloader=False,)

@stay_put
def compile_enaml(fpath):
    print "Compiling Enaml from", fpath
    abspath = os.path.abspath(fpath)
    os.chdir('app')
    path, fname = os.path.split(abspath)
    shutil.copy(abspath, fname)
    sys.path.insert(0, os.getcwd())
    import enaml_loader
    # Should spit out myapp.html to pwd
    enaml_loader.main()
    root, ext = os.path.splitext(fname)
    out_file = open(os.path.join('templates', root + '.html'), 'w')
    out_file.write(templatify_html(open(root + '.html')))
    out_file.close()

def _qt(args):
    compile_check(args)

    initial_port = args.port
    port = ashiba.utils.get_port('localhost', initial_port)
    server_args = copy.deepcopy(args)
    server_args.port = port
    server = mp.Process(target=_start, args=(server_args,))
    server.start()
    url = 'http://localhost:{}'.format(port)
    with stay():
        os.chdir(os.path.join(args.path, 'app'))
        sys.path.insert(0, os.getcwd())
        import settings
        if 'QT_ICON' in vars(settings):
            icon = os.path.abspath(settings.QT_ICON)
        elif 'APP_ICON' in vars(settings):
            icon = os.path.abspath(settings.APP_ICON)
        else:
            icon = ''

        if 'APP_NAME' in vars(settings):
            name = settings.APP_NAME
        else:
            name = os.path.split(args.path)[-1]
        name = "Ashiba: " + name

    browser = mp.Process(target=browse, args=(url, name, icon))
    browser.start()
    browser.join()
    # This stuff happens after Qt window is closed
    print "Qt window closed. Quitting."
    server.terminate()
    sys.exit()

def browse(url, name='', icon=''):
    from PySide.QtGui import QApplication, QIcon
    from PySide.QtCore import QUrl
    from PySide.QtWebKit import QWebView

    for try_ in range(10):
        try:
            assert urllib2.urlopen(url).code == 200
        except (AssertionError, urllib2.URLError):
            time.sleep(0.25)
        else:
            print "Started Qt Web View after %i ticks." % try_
            break
    else:
        sys.exit("Error initializing Qt Web View.")

    qtapp = QApplication(name)
    web = QWebView()
    web.load(QUrl(url))
    if icon:
        print "Setting Icon to", icon
        web.setWindowIcon(QIcon(icon))
    else:
        print "WARNING: No icon found in settings.py"
    web.setWindowTitle(name)
    web.show()
    qtapp.exec_()

@stay_put
def _build(args):
    path = args.path
    os.chdir(path)
    if os.getcwd() not in sys.path:
        sys.path.insert(0, os.getcwd())

    import settings
    SETTINGS = {k:v for k,v in vars(settings).items() \
                        if not k.startswith('__')}

    required_keys = ['APP_NAME']
    if len(set(required_keys) - set(SETTINGS.keys())):
        error_str = "ERROR: The following settings are missing from the settings.py file:"
        for key in set(required_keys) - set(SETTINGS.keys()):
            error_str += "\n* " + key
        sys.exit(error_str)

    app_head = os.path.split(os.getcwd())[-1]

    meta = {}
    meta['package'] = { 'name'    : app_head,
                        'version' : 0.0,
                        }
    meta['requirements'] = {}
    meta['requirements']['build'] = ['python']
    meta['requirements']['run'] = [
                        'python',
                        'pyside',
                        'matplotlib',
                        'ashiba',
                        ]
    meta['app'] = {     'entry'  : "ashiba qt ashiba/{}".format(app_head),
                        'type'   : 'web',
                        }
    if 'APP_ICON' in SETTINGS:
        meta['app']['icon'] = os.path.join('..', 'src',
                                app_head, SETTINGS['APP_ICON'])
    if 'APP_SUMMARY' in SETTINGS:
        meta['app']['summary'] = SETTINGS['APP_SUMMARY']

    binstar_path = SETTINGS.get('BINSTAR_ID', '')
    meta['about'] = {   'home'   : 'http://binstar.org/' + binstar_path,
                        'license': SETTINGS.get('LICENSE')
                        }

    build_dir = os.path.abspath('build')
    if os.path.isdir(build_dir):
        print "CLEAN: {}".format(build_dir)
        shutil.rmtree(build_dir)

    source_dir = os.path.join('build', 'src', app_head)
    temp_dir = os.path.join(tempfile.mkdtemp(), app_head)
    shutil.copytree(os.getcwd(), temp_dir)
    clean_app_dir(temp_dir)
    shutil.copytree(temp_dir, source_dir)
    os.mkdir(os.path.join(build_dir, 'conda-recipe'))
    recipe_dir = os.path.join(build_dir, 'conda-recipe')

    with closing(open(os.path.join(recipe_dir, 'meta.yaml'), 'w')) as f_out:
        f_out.write(ashiba.utils.prettyaml(meta))

    # These should probably be files in the current dir that get copied...

    build_sh = """mkdir $PREFIX/ashiba/
cp -r $RECIPE_DIR/../src/* $PREFIX/ashiba/"""
    with closing(open(os.path.join(recipe_dir, 'build.sh'), 'w')) as f_out:
        f_out.write(build_sh)

    build_bat = """md %PREFIX%\\ashiba
xcopy %RECIPE_DIR%\\..\\src\\* %PREFIX\\ashiba"""
    with closing(open(os.path.join(recipe_dir, 'build.bat'), 'w')) as f_out:
        f_out.write(build_bat)



def _help(args):
    print "Usage: ashiba [init|compile|start|qt|build|clean] <app_dir>"

def main():
    import argparse

    if len(sys.argv) == 1:
        sys.argv.append('-h')

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    init = subparsers.add_parser(
        "init",
        help="Initialize an empty Ashiba app",
        )
    init.set_defaults(func=_init)

    compile = subparsers.add_parser(
        "compile",
        help="Compile an app",
        )
    compile.set_defaults(func=_compile)

    start = subparsers.add_parser(
        "start",
        help="Run a compiled app in the browser",
        )
    start.add_argument(
        "--open-browser",
        default=False,
        action="store_true",
        help="Open the web browser (default=False)",
        )
    start.set_defaults(func=_start)

    qt = subparsers.add_parser(
        "qt",
        help="Run a compiled app in qt",
        )
    qt.set_defaults(func=_qt)

    build = subparsers.add_parser(
        "build",
        help="Create a conda-recipe of the web app in place in build/",
        )
    build.set_defaults(func=_build)

    clean = subparsers.add_parser(
        "clean",
        help="clean up the files created during the build command",
        )
    clean.set_defaults(func=_clean)

    for subparser in (init, compile, start, qt, build):
        subparser.add_argument('path', help='Path to Ashiba project.')

    clean.add_argument('paths', nargs='+', help='Paths to Ashiba projects.')

    port_kwargs = {
        'action': 'store',
        'default': 12345,
        'type':    int,
        'help':   "Start the web server on this port (default=12345)",
        }
    for subparser in (start, qt):
        subparser.add_argument('--port', **port_kwargs)
        subparser.add_argument(
            "--recompile",
            default=False,
            action="store_true",
            help="Force a recompile (default=False)",
            )

    args = parser.parse_args()

    args.func(args)
