# -*- coding: utf-8 -*-
"""
Various definitions used across different packages.
"""
from __future__ import absolute_import, division, print_function, unicode_literals

#### Authentication ####

# the scheme for authenticating clients.
AUTHENTICATION_SCHEME = 'eavatar'

# return to client to
AUTHENTICATION_HEADER = 'EAvatar realm="eavatar.com",key="abcd"'


VERSION_STRING = "0.1.0"

# return as the root resource.
AGENT_INFO = {
            "EAvatar": "A versatile agent.",
            "version": VERSION_STRING,
            "vendor": {
                "name": "EAvatar Technology Ltd.",
                "version": "0.1.0"
            },
}


# The ID for built-in message listener.
MESSAGE_LISTENER_ID = 'message'

MAX_MESSAGE_SIZE = 1024
MAX_REQUEST_SIZE = 4096


##### Environment variable ####
AVA_HOME = 'AVA_HOME'  # where the working directory.
AVA_SECRET_KEY = 'AVA_SECRET_KEY'  # secret key for this agent.
AVA_OWNER_KEY = 'AVA_OWNER_KEY'  # the owner's public key.