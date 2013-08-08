#!/usr/bin/python
# -*- coding: latin-1 -*

import re
import json

def temperature_convert(in_message):
    to_return = {'domDeltas': []}
    in_state = json.loads(in_message)
    if in_state['id'] == 'txt_celsius':
        c_temp = int(re.search('(-?\d+)', in_state['data']['value']).group(1))
        f_temp = c_temp * 9 / 5. + 32
        f_str = '{0:0.3g} F'.format(f_temp)
        delta = {'id' : 'txt_farenheit', 'data' : {'value' : f_str}}
    else:
        f_temp = int(re.search('(-?\d+)', in_state['data']['value']).group(1))
        c_temp = (f_temp - 32) * 5 / 9.
        c_str = '{0:0.3g} C'.format(c_temp)
        delta = {'id' : 'txt_celsius', 'data' : {'value' : c_str}}
    to_return['domDeltas'].append(delta)
    return json.dumps(to_return)
            
