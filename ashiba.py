import re, os, sys, shutil

__version__ = 0.0
ASHIBA_SHARE = os.path.join(os.getcwd(), 'ashiba_share')
print 'ASHIBA_SHARE:', ASHIBA_SHARE

def _compile(path, *args):
    os.chdir(path)
    if os.getcwd() not in sys.path:
        sys.path.insert(0, os.getcwd())

    import settings
    SETTINGS = {k:v for k,v in settings.__dict__.items() \
                        if not k.startswith('__')}
    import myapp

    if os.path.isfile('app'):
        sys.exit("Fatal: \
            There can't be a file named 'app' in the project dir.")
    elif os.path.isdir('app'):
        shutil.rmtree('app')

    shutil.copytree(
        os.path.join(ASHIBA_SHARE, 'compiled_project_files'), 
        'app')
    for fname in os.listdir('.'):
        ext = os.path.splitext(fname)[-1]
        if ext == '.py':
            shutil.copy(fname, os.path.join('app', fname))
        elif ext == '.html':
            shutil.copy(fname, os.path.join('app', 'templates', fname))

    if os.path.isdir('static'):
        for item in [os.path.join('static', x) for x in os.listdir('static')]:
            src, dst = item, os.path.join('app', item)
            if os.path.isdir(item):
                shutil.copytree(src, dst)
            else:
                shutil.copy(src, dst)

    file_path = os.path.join('app','static','ashiba_compiled.js')
    print "Writing to:", os.path.abspath(file_path)
    outfile = open(file_path, 'w')
    outfile.write("/* Compiled with Ashiba v{} */\n".format(__version__))
    outfile.write("\n$(window).load(function(){")
    fcn_names = [k for k in myapp.__dict__ if re.match('[\w]+?__[\w]+', k)]

    for fcn_name in fcn_names:
        print "Translating", fcn_name
        name, event = fcn_name.rsplit('__', 1)
        jquery_string = """
  $("#{name}").on("{event}",
    ashiba.eventHandlerFactory("{name}", "{event}")
  );""".format(name=name,event=event)

        outfile.write(jquery_string)

    outfile.write("\n});") #end document.ready
    outfile.close()

    ## Put the boilerplate header on top of the html

def _init(path, *args):
    print "Init:", path
    if os.path.exists(path):
        sys.exit("Fatal: Path '{}' already exists.".format(
            os.path.abspath(path)))
    shutil.copytree(os.path.join(ASHIBA_SHARE, 'new_project_files'), path)

def _start(path, *args):
    app_path = os.path.join(path, 'app')
    if os.path.isdir(app_path):
        os.chdir(app_path)
        if os.getcwd() not in sys.path:
            sys.path.insert(0, os.getcwd())
    else:
        sys.exit("Compiled app path not found. Run 'compile' first.")
    import flask_loader
    print "Running webserver in dir:", os.getcwd()
    flask_loader.app.run(host='localhost', port=12345, debug=True, threaded=True)

def _help(*args):
    print "Usage: ashiba [init|compile|start] <app_dir>"

if __name__ == "__main__":
    command = sys.argv[1].strip() if len(sys.argv) > 1 else 'help'
    args = sys.argv[2:] if len(sys.argv) > 2 else []
    {'compile': _compile,
     'init'   : _init,
     'start'  : _start}.get(command, _help)(*args)
