import re
import sys, os
import json

import flask
from flask import Flask, Response, redirect, render_template, request, url_for

from geventwebsocket.handler import WebSocketHandler
from gevent.pywsgi import WSGIServer

import handlers
import settings

app = Flask(__name__)
SETTINGS = {k:v for k,v in settings.__dict__.items() 
                    if not k.startswith('__')}

@app.route('/')
def render_app():
    if SETTINGS.get('FAVICON'):
        favicon = SETTINGS['FAVICON']
    else:
        favicon = SETTINGS.get('APP_ICON')
    app_name = SETTINGS.get('APP_NAME', 'My App')
    return render_template('myapp.html',
                            favicon=favicon,
                            app_name=app_name)

@app.route('/api', methods=['GET', 'POST'])
def api():
    if request.environ.get('wsgi.websocket'):
        ws = request.environ['wsgi.websocket']
        while True:
            in_message = ws.receive()
            print "MESSAGE RECEIVED:", in_message
            out_message = handlers.temperature_convert(in_message)
            ws.send(out_message)
            print "MESSAGE SENT:", out_message 
    return

if __name__ == "__main__":
    print "Running webserver in dir:", os.getcwd()
    #app.run(host='localhost', port=12345, debug=True) #, threaded=True)
    app.debug = True
    http_server = WSGIServer(('',12345), app, handler_class=WebSocketHandler)
    http_server.serve_forever()
