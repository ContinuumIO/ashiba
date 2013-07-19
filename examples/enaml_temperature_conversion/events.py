#!/usr/bin/python
# -*- coding: latin-1 -*

import re

#Probably going to have to have a 'this' as well as dom.
def btn_convert__click(dom):
    # Everything is a string, gotta validate.
    temp_str = dom['txt_temperature']['value'].strip()
    rex = re.match('([+-]?\d+\.?\d*)\s*([CcFf])', temp_str)
    if not rex:
        print "ERROR: INVALID TEMP"
        raise ValueError("Invalid temp. Did you forget a unit?")
    else:
        temp = float(rex.group(1))
        unit = rex.group(2).upper()

    if unit == 'C':
        converted_temp = 9 / 5.0 * temp + 32
        suffix = 'F'
    elif unit == 'F':
        converted_temp = (temp - 32) * 5.0 / 9
        suffix = 'C'

    new_temp_str = "{0:0.3g} {1}".format(converted_temp, suffix)

    dom['txt_temperature']['value'] = new_temp_str
    return dom
