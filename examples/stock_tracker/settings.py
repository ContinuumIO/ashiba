## In this file, you set some app-wide settings.
import os

APP_NAME = "My Awesome Ashiba App"
APP_ICON = "static/img/ca_icon.png"
QT_ICON  = "static/img/ca_icon_256.png"

# Those settings can be python expressions!
DATA_FILES = [x for x in os.listdir('.') if x.endswith('.csv')]

APP_THEME = "cyborg"
## Default installed themes:
#  [amelia, cerulean, cyborg, flatly, journal, 
#   readable, simplex, slate, spacelab, united,]
