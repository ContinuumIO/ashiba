
from atom.api import Unicode

from enaml.core.declarative import d_

from html_object import HTMLObject
from lxml.html import builder as E

class List(HTMLObject):

    tag = E.UL
    text = d_(Unicode())

    def initialize(self):
        super(List, self).initialize()

    def buildHTML(self, *args):
        self.addTags()
        self.addText(self.text)
        self.addAttributes()

        return super(List, self).buildHTML(*args)