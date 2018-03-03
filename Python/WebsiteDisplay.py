#!/usr/bin/python3

import os

# Make the json print functionality work with both Python 2 and 3
try:
    to_unicode = unicode
except NameError:
    to_unicode = str
    
# Directory that has the CCBC webpage. 
# Note that directory is different depending on operating system
# Windows: C:\xampp\htdocs\CCBC
# Linux: /var/www/html
# TODO: make this an if statement
html_dir = os.path.join("C:", "xampp", "htdocs", "CCBC")