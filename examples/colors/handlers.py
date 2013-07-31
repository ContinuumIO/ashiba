## This file is where you write your event handlers in Python.
## Define functions named like element_id__event(dom) e.g.
#   btn_mybutton__click(dom):
#       dom['txt_textbox']['value'] = "Button clicked."
#   return dom
#
## You can delete this comment once you've read it.

def get_colors(dom):
    return [dom[x]['value'] for x in ['slider_R', 'slider_G', 'slider_B']]

def set_colors(dom):
    R, G, B = get_colors(dom)
    dom['tabs'].style('background-color', 'rgb({}, {}, {})'.format(R, G, B))

## Wouldn't it be nice to use a class selector? 
## Perhaps single underscore? Or maybe move to decorators?

def slider_R__change(dom):
    set_colors(dom)
    return dom

def slider_G__change(dom):
    set_colors(dom)
    return dom

def slider_B__change(dom):
    set_colors(dom)
    return dom

def btn_color__click(dom):
    dom['dialog'].body = "<p>This color is RGB({}, {}, {}).</p>".format(
        *get_colors(dom))
    dom['dialog'].add_class('spam')
    #dom['dialog']['title'] = "Lovely Spam"
    dom['dialog'].title = "Lovely Spam"
    return dom
