#!/usr/bin/env python3

import os
import sys

ROOT_FOLDER = os.path.abspath('.')
LOGS_FOLDER = os.path.join(ROOT_FOLDER, '..', 'Logs')
PYTHON_PACKAGE = os.path.join(ROOT_FOLDER, 'Python')

# Ensure that the packages folder is in the path
sys.path.extend([PYTHON_PACKAGE])
