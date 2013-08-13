
from atom.api import Unicode, List, Dict

from enaml.core.declarative import Declarative
from enaml.core.declarative import d_

class HTMLObject(Declarative):

    tag = None #Tag for HTML Object

    objectIds = {}

    id = Unicode() #Id of HTML Object
    extraTags = List() #List of Extra Tags added
    textList = List() #List of Text Values
    attributeDict = Dict() #Dictionary of HTML Attributes

    def initialize(self):
        if self.id:
            print "Adding Object Id:", self.id
            self.objectIds[self.id] = self

    	super(HTMLObject, self).initialize()

    @classmethod
    def updateObject(self, id, value):
        for myid, object in self.objectIds.iteritems():
            if myid == id:
                object.value = value
                break

    def addAttributes(self, **kwargs):
        for key, value in kwargs.iteritems():
            self.attributeDict[key] = value

    def addTags(self, *args):
        self.extraTags += args

    def addText(self, *args):
        self.textList += args

    def buildHTML(self, *args):
        if self.extraTags:
            args = tuple(self.extraTags) + args 
        if self.textList:
    	    args += tuple(self.textList)
        
        return self.tag(*args, **self.attributeDict)
    
    def _update_web(self, change):
        from web_com import WebCom
        WebCom.enamltoWeb(change)
