
from atom.api import Unicode

from enaml.core.declarative import d_

from html_generator import HTMLGenerator
from html_object import HTMLObject

import lxml
from lxml.html import builder as E

class Window(HTMLObject):

    tag = E.DIV
    id = d_(Unicode())
    def initialize(self):
        super(Window, self).initialize()

    def destroy(self):
        super(Window, self).destroy()

    def buildHTML(self, *args):
        self.addTags()
        self.addText()
        self.addAttributes()

        return super(Window, self).buildHTML(*args)

    def show(self):
        htmlGenerator = HTMLGenerator()
        htmlGenerator.addHTML(htmlGenerator.buildChildren(self))
        htmlGenerator.dumpHTML()
        self.initialize()

    def generateHTML(self):
        htmlGenerator = HTMLGenerator()
        htmlGenerator.addHTML(htmlGenerator.buildChildren(self))
        print lxml.html.tostring(htmlGenerator.getHTML())
        with open('myapp.html', 'w') as f:
            f.write(lxml.html.tostring(htmlGenerator.getHTML()))


        

    





        
    
