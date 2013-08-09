## This file is where you write your event handlers in Python.
## Define functions named like element_id__event(dom) e.g.
#   btn_mybutton__click(dom):
#       dom['txt_textbox']['value'] = "Button clicked."
#   return dom
#
## You can delete this comment once you've read it.
import pandas as pd

import ashiba

df = pd.DataFrame.from_csv('census_marriage.csv', index_col=None)

def btn_load__click(dom):
    dom['my_table'] = ashiba.dom.DataTable(data=df)
