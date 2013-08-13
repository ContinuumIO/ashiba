
from atom.api import Unicode

from enaml.core.declarative import d_

from html_object import HTMLObject
from lxml.html import builder as E

class Checkbox(HTMLObject):

    tag = E.INPUT
    text = d_(Unicode())

    def initialize(self):
        super(Checkbox, self).initialize()

    def buildHTML(self, *args):
        self.addTags()
        self.addText(self.text)
        self.addAttributes(type = "checkbox")

        return super(Checkbox, self).buildHTML(*args)