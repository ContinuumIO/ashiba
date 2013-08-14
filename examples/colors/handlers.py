## This file is where you write your event handlers in Python.
## Define functions named like element_id__event(dom) e.g.
#   btn_mybutton__click(dom):
#       dom['txt_textbox']['value'] = "Button clicked."
#   return dom
#
## You can delete this comment once you've read it.
import urllib2

def get_colors(dom):
    return [dom[x]['value'] for x in ['slider_R', 'slider_G', 'slider_B']]

def _color_control__change(dom):
    R, G, B = get_colors(dom)
    dom['my_tabs'].style('background-color', 'rgb({}, {}, {})'.format(R, G, B))

def btn_color__click(dom):
    dom['dialog'].body = "<p>This color is RGB({}, {}, {}).</p>".format(
        *get_colors(dom))
    dom['dialog'].add_class('spam')
    #dom['dialog']['title'] = "Lovely Spam"
    dom['dialog'].title = "Lovely Spam"
    return dom

def btn_fortune__click(dom):
    resp = urllib2.urlopen('http://www.iheartquotes.com/api/v1/random')
    text = resp.read()
    dom['my_tabs'].add_tab('My Fortune', text)
    return dom
