
from atom.api import Unicode, Dict

from enaml.core.declarative import d_

from html_object import HTMLObject
from lxml.html import builder as E

class Date(HTMLObject):

    tag = E.INPUT

    text = d_(Unicode())
    id = d_(Unicode())

    date = d_(Dict())

    def initialize(self):
        super(Date, self).initialize()

    def buildHTML(self, *args):
        self.addTags()
        self.addText(self.text)
        self.addAttributes()

        if self.id:
            self.addAttributes(type = "date", id = self.id)

        return super(Date, self).buildHTML(*args)

    #@observe(('date'))
    def _update_web(self, change):
        super(Date, self)._update_web(change)