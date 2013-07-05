import sys, os
import copy
import json
import pprint

import flask
from flask import Flask, Response, redirect, render_template, request, url_for

import ashiba.utils
import myapp
import settings

app = Flask(__name__)
SETTINGS = {k:v for k,v in settings.__dict__.items() 
                    if not k.startswith('__')}

@app.route('/event/<obj_id>/<event>', methods=['POST'])
def fire_event(obj_id, event):
    fcn_name = "{}__{}".format(obj_id, event)
    fcn = myapp.__dict__.get(fcn_name)
    if not fcn:
        return 'Event function not found.', 404
    print "REQUEST RECEIVED:"
    print request.data
    print ""
    if not request.data:
        return 'No data included.', 200
    
    try:
        dom = ashiba.utils.autovivify(json.loads(request.data))
        new_dom = fcn(copy.deepcopy(dom))
    except ValueError, e:
        return e.message, 400
    
    dom_changes = ashiba.utils.dict_diff(new_dom, dom)
    print "DOM CHANGES:"
    pprint.pprint(dom_changes)
    return flask.jsonify({'success'    :True,
                          'dom_changes':dom_changes})

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
            
if __name__ == "__main__":
    print "Running webserver in dir:", os.getcwd()
    app.run(host='localhost', port=12345, debug=True, threaded=True)
