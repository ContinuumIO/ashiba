
from atom.api import Unicode

from enaml.core.declarative import d_

from html_object import HTMLObject
from lxml.html import builder as E

class Row(HTMLObject):

    tag = E.DIV

    def initialize(self):
        super(Row, self).initialize()

    def buildHTML(self, *args):
        self.addTags()
        self.addText()
        kwargs = {'class':"row"}
        self.addAttributes(**kwargs)

        return super(Row, self).buildHTML(*args)