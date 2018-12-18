#!/usr/bin/python3

# Import standard Python files
import os
import io

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


class WebsiteUpdate(object):
    """ Contains functionality related to the website"""

    @staticmethod
    def write_json_file(directory, dictionary):
        # Write a json file using the dictionary
        with io.open(os.path.join(directory, "ccbc.json"),
                     "w", encoding='utf8') as outfile:
            str_ = json.dumps(dictionary,
                              indent=4, sort_keys=True,
                              separators=(',', ': '), ensure_ascii=False)
            outfile.write(to_unicode(str_))
        return str_
