
from atom.api import Unicode

from enaml.core.declarative import d_

from html_object import HTMLObject
from lxml.html import builder as E

class Button(HTMLObject):

    tag = E.BUTTON

    text = d_(Unicode())
    id = d_(Unicode())

    def initialize(self):
        super(Button, self).initialize()

    def buildHTML(self, *args):
        self.addTags()
        self.addText(self.text)
        self.addAttributes()

        if self.id:
            self.addAttributes(id = self.id)

        return super(Button, self).buildHTML(*args)
