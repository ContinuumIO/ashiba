## This file is where you write your event handlers in Python.
## Define functions named like element_id__event(dom) e.g.
#   btn_mybutton__click(dom):
#       dom['txt_textbox']['value'] = "Button clicked."
#   return dom
#
## You can delete this comment once you've read it.

import random

def btn_shuffle__click(dom):
    car_list = dom['select'].list_items()
    random.shuffle(car_list)
    dom['select'].empty()
    dom['select'].add_items(car_list)
    return dom
