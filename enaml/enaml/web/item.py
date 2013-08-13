
from atom.api import Unicode

from enaml.core.declarative import d_

from html_object import HTMLObject
from lxml.html import builder as E

class Item(HTMLObject):

    tag = E.LI
    text = d_(Unicode())

    def initialize(self):
        super(Item, self).initialize()

    def buildHTML(self, *args):
        self.addTags()
        self.addText(self.text)
        self.addAttributes()

        return super(Item, self).buildHTML(*args)