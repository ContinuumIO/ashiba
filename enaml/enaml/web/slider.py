
from atom.api import Unicode, Int

from enaml.core.declarative import d_

from html_object import HTMLObject
from lxml.html import builder as E

class Slider(HTMLObject):

    tag = E.INPUT

    text = d_(Unicode())
    id = d_(Unicode())
    value = d_(Int())
    min = d_(Int())
    max = d_(Int())

    def initialize(self):
        super(Slider, self).initialize()

    def buildHTML(self, *args):
        self.addTags()
        self.addText(self.text)
        self.addAttributes(id = self.id, type = "range", value = str(self.value), min = str(self.min), max = str(self.max))
        return super(Slider, self).buildHTML(*args)