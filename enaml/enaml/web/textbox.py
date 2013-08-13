
from atom.api import Unicode, observe

from enaml.core.declarative import d_

from html_object import HTMLObject
from lxml.builder import E

class Textbox(HTMLObject):

    tag = E.input

    text = d_(Unicode())
    id = d_(Unicode())
    value = d_(Unicode())

    def initialize(self):
        super(Textbox, self).initialize()

    def buildHTML(self, *args):
        self.addTags()
        self.addText()
        self.addAttributes(type = "text")

        if self.id:
            self.addAttributes(id = self.id)

        if self.value:
            self.addAttributes(value = self.value)
            attrs = {'data-events':'change', 'data-visible':'value'}
            self.addAttributes(**attrs)

        return super(Textbox, self).buildHTML(*args)

    @observe(('value'))
    def _update_web(self, change):
        super(Textbox, self)._update_web(change)
