
from atom.api import Unicode, Int

from enaml.core.declarative import d_

from html_object import HTMLObject
from lxml.html import builder as E

class Input(HTMLObject):

    tag = E.INPUT

    type = d_(Unicode())
    text = d_(Unicode())
    id = d_(Unicode())
    name = d_(Unicode())

    min = d_(Int())
    max = d_(Int())

    def initialize(self):
        super(Input, self).initialize()

    def buildHTML(self, *args):
        self.addTags()
        self.addText(self.text)
        self.addAttributes(type = self.type)

        if self.id:
            self.addAttributes(id = self.id)
        if self.name:
            self.addAttributes(name = self.name)
        if self.min:
            self.addAttributes(min = str(self.min))
        if self.max:
            self.addAttributes(max = str(self.max))

        return super(Input, self).buildHTML(*args)
