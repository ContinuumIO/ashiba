## In this file, you set some app-wide settings.
import os

APP_NAME = "My Awesome Ashiba App"
APP_ICON = "static/img/ca_icon.png"

# Those settings can be python expressions!
DATA_FILES = [x for x in os.listdir('.') if x.endswith('.csv')]
