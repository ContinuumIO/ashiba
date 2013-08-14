
import os

from lxml import etree
import lxml
from lxml.html import builder as E

class HTMLGenerator:

	html = E

	def __init__(self):
		pass

	def addHTML(self, *args):
		self.html = E.HTML(*args)

	def getHTML(self):
		return self.html
		
	def dumpHTML(self):
		print etree.tostring(self.html)
		with open(os.getcwd() + '/templates/myapp.html', 'w') as f:
			f.write ("{% extends \"app_template.html\" %}\n{% block content %}\n")
			f.write(lxml.html.tostring(self.html))
			f.write("\n{% endblock content %}")

	def buildChildren(self, current):
		if current.children:
			data = []
			for child in current.children:
				data.append(self.buildChildren(child))
			return current.buildHTML(*data)

		return current.buildHTML()