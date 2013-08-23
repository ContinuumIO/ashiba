import sys, os
import copy
import json
import uuid
import pprint

import flask
from flask import Flask, Response, redirect, render_template, request, url_for

import ashiba.utils
import ashiba.dom
import handlers
import settings

app = Flask(__name__)
SETTINGS = {k:v for k, v in vars(settings).items()
                    if not k.startswith('__')}

try:
    debug = SETTINGS['DEBUG']
except:
    debug = False
    
@app.route('/event/<obj_id>/<event>', methods=['POST'])
def fire_event(obj_id, event):
    fcn_name = "{}__{}".format(obj_id, event)
    if fcn_name in vars(handlers):
        fcn = vars(handlers)[fcn_name]
    elif ('_' + fcn_name) in vars(handlers):
        fcn = vars(handlers)['_' + fcn_name]
    else:
        return 'Event function not found.', 404
    print "REQUEST RECEIVED:"
    if debug:
        print pprint.pprint(request.data)
        #An extra None gets printed here. Why?
        print ""
    
    if not request.data:
        print "Error: no data sent in request."
        return 'No data included.', 200

    try:
        dom = ashiba.dom.Dom(json.loads(request.data))
        fcn(dom)
    except ValueError, e:
        print e.message
        return e.message, 400

    dom_changes = dom.changes()
    if debug:
        print "DOM CHANGES:"
        pprint.pprint(dom_changes)
        print ""
    
    print "SENDING RESPONSE..."
    return flask.jsonify({'success'    :True,
                          'dom_changes':dom_changes})

@app.route('/')
def render_app():
    if SETTINGS.get('FAVICON'):
        favicon = SETTINGS['FAVICON']
    else:
        favicon = SETTINGS.get('APP_ICON')

    theme = SETTINGS.get('APP_THEME')

    app_name = SETTINGS.get('APP_NAME', 'My App')

    return render_template('myapp.html',
                            favicon=favicon,
                            theme=theme,
                            app_name=app_name,
                            uuid=uuid.uuid4(),
                            )

if __name__ == "__main__":
    print "Running webserver in dir:", os.getcwd()
    app.run(host='localhost', port=12345, debug=True) #, threaded=True)
