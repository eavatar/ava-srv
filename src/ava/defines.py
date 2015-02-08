# -*- coding: utf-8 -*-
"""
Various definitions used across different packages.
"""
from __future__ import absolute_import, division, print_function, unicode_literals


VERSION_STRING = "0.1.0"
VERSION_MAJOR = 0
VERSION_MINOR = 1
VERSION_MICRO = 0

# return as the root resource.
AGENT_INFO = {
    "EAvatar": "A versatile agent.",
    "version": VERSION_STRING,
    "vendor": {
        "name": "EAvatar Technology Ltd.",
        "version": "0.1.0"
    },
}


# activated engines

INSTALLED_ENGINES = [
    "ava.engine.data:DataEngine",
    "ava.engine.webfront:WebfrontEngine",
    "ava.engine.extension:ExtensionEngine",
    "ava.engine.module:ModuleEngine",
]


##### Environment variable ####
AVA_HOME = 'AVA_HOME'  # where the working directory.
AVA_SECRET_KEY = 'AVA_SECRET_KEY'  # secret key for this agent.
AVA_OWNER_KEY = 'AVA_OWNER_KEY'  # the owner's public key.


# tries to import definitions from the global settings.

try:
    from settings import *
except ImportError:
    pass