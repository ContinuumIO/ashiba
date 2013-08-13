import os
import json

import flask
import settings
from flask import Flask, Response, redirect, render_template, request, url_for

from geventwebsocket.handler import WebSocketHandler
from gevent.pywsgi import WSGIServer

from ashiba.utils import get_port

from web_com import WebCom

app = Flask(__name__,
            template_folder = os.path.join(os.getcwd(), 'templates'),
            static_folder = os.path.join(os.getcwd(), 'static'),
            )

SETTINGS = {k:v for k,v in vars(settings).items()
                   if not k.startswith('__')}

@app.route('/')
def render_app():
    if SETTINGS.get('FAVICON'):
        favicon = SETTINGS['FAVICON']
    else:
        favicon = SETTINGS.get('APP_ICON')
    app_name = SETTINGS.get('APP_NAME', 'My App')
    return render_template('myapp.html',
                            app_name=app_name)


@app.route('/api', methods=['GET', 'POST'])
def api():
    if request.environ.get('wsgi.websocket'):
        ws = request.environ['wsgi.websocket']
        while True:
            in_message = ws.receive()
            print "MESSAGE RECEIVED:", in_message

            WebCom.webtoEnaml(json.loads(in_message), ws)
    return

def start():
    app.debug = True
    port = get_port('localhost', 12345)
    print "Starting server on port %i from dir %s" % (port, os.getcwd())
    http_server = WSGIServer(('',port), app, handler_class=WebSocketHandler)
    http_server.serve_forever()
