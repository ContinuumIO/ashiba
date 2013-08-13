from atom.api import Typed

from enaml.application import Application
import flask_loader

class WebApplication(Application):
    
    def __init__(self):
        super(WebApplication, self).__init__()
        
    def start(self):
        flask_loader.start()
        
    def stop(self):
        print "Stop Application"


    
        