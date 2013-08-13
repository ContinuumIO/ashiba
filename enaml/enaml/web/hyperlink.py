
from atom.api import Unicode

from enaml.core.declarative import d_

from html_object import HTMLObject
from lxml.html import builder as E

class Hyperlink(HTMLObject):

    tag = E.A
    text = d_(Unicode())
    id = d_(Unicode())
    type = d_(Unicode())

    def initialize(self):
        super(Hyperlink, self).initialize()

    def buildHTML(self, *args):
        self.addTags()
        self.addText(self.text)
        kwargs = {'class': self.type, 'id': self.id}
        self.addAttributes(**kwargs)

        return super(Hyperlink, self).buildHTML(*args)