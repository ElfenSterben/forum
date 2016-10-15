#!/usr/bin/env python3

import sys
from os.path import abspath
from os.path import dirname

sys.path.insert(0, abspath(dirname(__file__)))
from app import configured_app

app = configured_app()
application = app
