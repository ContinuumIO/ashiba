## This file is where you write your event handlers in Python.
## Define functions named like element_id__event(dom) e.g.
#   btn_mybutton__click(dom):
#       dom['txt_textbox']['value'] = "Button clicked."
#   return dom
#
## You can delete this comment once you've read it.
import pandas as pd

import ashiba
import ashiba.plot
from ashiba.plot import plt

df = pd.DataFrame.from_csv('census_marriage.csv', index_col=None)
"""
Sex
1       Male
2       Female

Status
4       Divorced
1       Married
2       Married, Spouse Absent
3       Separated
6       Single
0       Unknown
5       Widowed
"""

#def btn_load__click(dom):
def _plot_control__change(dom):
    year = int(dom['slider_year']['value'])
    sex = None
    if dom['radio_male']['checked']:
        sex = 1
    elif dom['radio_female']['checked']:
        sex = 2
    if year == 1890 or sex is None:
        return

    subset = df[df.year == year][df.sex == sex][df.age >= 15]
    # Does this need to be a new instantiation?
    dom['my_table'] = ashiba.dom.DataTable(data=subset)
    pivot = subset.pivot('age', 'marst', 'people')
    if 3 not in pivot:
        pivot[3] = [0]*len(pivot)
    pivot.plot(kind='bar', stacked=True, sort_columns=True)
    gender = {1:'male', 2:'female'}[sex]
    plt.title('Marriage records for year {}, {}'.format(year, gender))
    statuses = ('Unknown',
                'Married',
                'Married, Spouse Absent',
                'Separated',
                'Divorced',
                'Widowed',
                'Single',
                )
    plt.legend(statuses)
    dom['img_plot'].set_image(plt.get_svg(), 'svg')
    plt.close()
