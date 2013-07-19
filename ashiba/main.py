import re
import sys
import json
import time
import shutil
import urllib2
import os, os.path
import multiprocessing as mp
from contextlib import closing, contextmanager

import ashiba, ashiba.utils

ASHIBA_SHARE = os.path.join(os.path.dirname(__file__), 'share')
print 'ASHIBA_SHARE:', ASHIBA_SHARE

@contextmanager
def stay():
    oldcwd = os.getcwd()
    yield
    os.chdir(oldcwd)

def stay_put(fcn):
    def decorated_fcn(*args, **kwargs):
        oldcwd = os.getcwd()
        try:
            return fcn(*args, **kwargs)
        finally:
            os.chdir(oldcwd)
    return decorated_fcn


def get_mtimes(path):
    mtimes = {}
    for root, dirs, files in os.walk(path):
        if not root.startswith(os.path.join('.', path, '/app')):
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
    SETTINGS = {k:v for k,v in settings.__dict__.items() \
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
    fcn_names = [k for k in handlers.__dict__ if re.match('[\w]+?__[\w]+', k)]

    for fcn_name in fcn_names:
        print "--> Translating", fcn_name
        name, event = fcn_name.rsplit('__', 1)
        jquery_string = """
  $("#{name}").on("{event}",
    ashiba.eventHandlerFactory("{name}", "{event}")
  );""".format(name=name,event=event)

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
    path = args.path
    app_dir = os.path.join(path, 'app')
    if os.path.isdir(app_dir):
        print "CLEAN: {}".format(app_dir)
        shutil.rmtree(app_dir)
    
    modified = os.path.join(path, '.modified.json')
    if os.path.isfile(modified):
        os.remove(modified)

def _start(args):
    path = args.path
    app_path = os.path.abspath(os.path.join(path, 'app'))

    mtimes = get_mtimes(path)
    mtime_fname = os.path.abspath(os.path.join(path, '.modified.json'))
    try:
        old_mtimes = json.load(open(mtime_fname))
    except (IOError, ValueError):
        old_mtimes = {}
    if not os.path.isdir(app_path) or mtimes != old_mtimes:
        print "--- RECOMPILING before start ---"
        _compile(args)
        mtimes = get_mtimes(path)

    with closing(open(mtime_fname, 'w')) as mtime_file:
        json.dump(mtimes, mtime_file)
    
    print "APP_PATH:", app_path
    sys.path.insert(0, app_path)
    os.chdir(app_path)

    host, port = 'localhost', '12345'
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
    url = 'http://localhost:12345'
    name = os.path.split(args.path)[-1]
    server = mp.Process(target=_start, args=(args,))
    server.start()
    browser = mp.Process(target=browse, args=(url, name))
    browser.start()
    browser.join()
    # This stuff happens after Qt window is closed
    print "Qt window closed. Quitting."
    server.terminate()
    sys.exit()

def browse(url, name=''):
    from PySide.QtGui import QApplication
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
    web.show()
    qtapp.exec_()

def _help(args):
    print "Usage: ashiba [init|compile|start|clean] <app_dir>"

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('command', help='Ashiba command: [init|compile|start|clean]')
    parser.add_argument('path', help='Path to Ashiba project.')
    args_in = parser.parse_args()

    command = args_in.command
    {'compile': _compile,
     'init'   : _init,
     'start'  : _start,
     'clean'  : _clean,
     'qt'     : _qt,
    }.get(command, _help)(args_in)
