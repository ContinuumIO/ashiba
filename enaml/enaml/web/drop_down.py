
from atom.api import Unicode, List, Dict

from enaml.core.declarative import d_

from html_object import HTMLObject
from lxml.html import builder as E

class Dropdown(HTMLObject):

    tag = E.SELECT
    text = d_(Unicode())
    id = d_(Unicode())
    options = d_(Dict())

    def initialize(self):
        super(Dropdown, self).initialize()

    def buildHTML(self, *args):
        for key, value in self.options.iteritems():
            self.addTags(E.OPTION(value, value = key))
        self.addText(self.text)
        if self.id:
            self.addAttributes(id = self.id)

        return super(Dropdown, self).buildHTML(*args)