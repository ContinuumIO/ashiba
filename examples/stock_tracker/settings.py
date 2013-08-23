## In this file, you set some app-wide settings.
import os

# Set to True to get more output in the server console.
DEBUG = False

APP_NAME = "Stock Tracker"
APP_ICON = "static/img/ca_icon.png"
QT_ICON  = "static/img/ca_icon_256.png"

# The settings can be python expressions!
DATA_FILES = [x for x in os.listdir('.') if x.endswith('.csv')]

APP_THEME = "flatly"
## Default installed themes from http://bootswatch.com/:
#  [amelia, cerulean, cyborg, flatly, journal, 
#   readable, simplex, slate, spacelab, united,]
