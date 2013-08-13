
import json
from html_object import HTMLObject

class WebCom:

    ws = None

    def __init__(self):
        pass

    @classmethod
    def enamltoWeb(cls, change):        
        jsonDict = dict()
        jsonDict['id'] = change['object'].id
        jsonDict['data'] = {"value":change['value']}
        print "Message SENT:", [jsonDict]
        cls.ws.send(json.dumps({"domDeltas":[jsonDict]}))

    @classmethod
    def webtoEnaml(cls, in_message, ws):
        cls.ws = ws
        print in_message
        HTMLObject.updateObject(in_message['id'], in_message['data']['value'])

        
