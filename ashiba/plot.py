import io

import matplotlib as mpl
mpl.use('svg')
import matplotlib.pyplot as plt

def plt_method(f):
    setattr(plt, f.__name__, f)
    return f

@plt_method
def get_svg():
    svg = io.StringIO()
    plt.savefig(svg)
    return svg.getvalue()
