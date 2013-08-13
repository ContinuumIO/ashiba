
from atom.api import Unicode

from enaml.core.declarative import d_

from html_object import HTMLObject
from lxml.html import builder as E

class Form(HTMLObject):

    tag = E.FORM

    text = d_(Unicode())
    title = d_(Unicode())

    def initialize(self):
        super(Form, self).initialize()

    def buildHTML(self, *args):
        if self.title:
            self.addTags(E.H3(self.title))
        self.addText(self.text)
        self.addAttributes()

        return super(Form, self).buildHTML(*args)


