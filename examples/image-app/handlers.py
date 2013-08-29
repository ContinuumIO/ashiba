import ashiba   
from ashiba.plot import plt
import urllib, cStringIO
from processing import dominant_colors


global img_url 
img_url = "http://upload.wikimedia.org/wikipedia/commons/thumb/4/46/Greenland_scenery.jpg/800px-Greenland_scenery.jpg"

def get_image(URL):
    file = cStringIO.StringIO(urllib.urlopen(URL).read())
    return file


def btn_colors__click(dom):
        #img_url = dom['url']

    img_file = get_image(img_url)

    (primary, second, third, fourth, fifth, sixth) = dominant_colors(img_file)

    

    dom['dominantColor'].style('background', primary)
    dom['palette1'].style('background', second)
    dom['palette2'].style('background', third)
    dom['palette3'].style('background', fourth)
    dom['palette4'].style('background', fifth)
    dom['palette5'].style('background', sixth)

    return dom

def updateImage__click(dom):
   
    global img_url
    img_url = dom['imageUrl']['value']
    dom['img_plot'].attr('src', img_url)

    print img_url
    return dom