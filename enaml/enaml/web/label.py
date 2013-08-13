
from atom.api import Unicode

from enaml.core.declarative import d_

from html_object import HTMLObject
from lxml.html import builder as E

class Label(HTMLObject):

    tag = E.LABEL
    text = d_(Unicode())

    def initialize(self):
        super(Label, self).initialize()

    def buildHTML(self, *args):
        self.addTags()
        self.addText(self.text)
        self.addAttributes()

        return super(Label, self).buildHTML(*args)

    