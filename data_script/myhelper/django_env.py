
import os
import sys
from data_script import *


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_DIR = os.path.join(BASE_DIR,'web_iiiedu')
# print(BASE_DIR)
# print(PROJECT_DIR)

BASE_DIR = sys.path.append(PROJECT_DIR)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "web_iiiedu.settings")

import django
django.setup()
