
from atom.api import Unicode, Int

from enaml.core.declarative import d_

from html_object import HTMLObject
from lxml.html import builder as E

class Column(HTMLObject):

    tag = E.DIV
    width = d_(Int())
    id = d_(Unicode())

    def initialize(self):
        super(Column, self).initialize()

    def buildHTML(self, *args):
        self.addTags()
        self.addText()
        
        kwargs = {'class':"span" + str(self.width)}
        if self.id:
            kwargs['id'] = self.id
        self.addAttributes(**kwargs)

        return super(Column, self).buildHTML(*args)