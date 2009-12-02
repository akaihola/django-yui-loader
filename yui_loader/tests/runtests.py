#!/usr/bin/env python

import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
os.environ['DJANGO_SETTINGS_MODULE'] = 'yui_loader.tests.settings'

from django.core.management import call_command
call_command('test')
