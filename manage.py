#!/usr/bin/env python
import os
import sys

import dotenv
"""
If there's a DOTENV environment variable passed, read the environment variables from 
the passed location. Otherwise, by default, look for a .env file with the environment
variables to load
"""
dotenv.read_dotenv(os.environ.get('DOTENV', None)) 

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "etd_drop.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
