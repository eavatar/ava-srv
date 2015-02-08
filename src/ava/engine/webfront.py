# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import os
import sys
import glob
import logging
import gevent
from gevent import pywsgi
import bottle

from ava.runtime import config
from ava.runtime import environ

logger = logging.getLogger(__name__)

_RESOURCES_DIR = 'resources'

# the global web application
app = bottle.app()


class WebfrontEngine(object):
    """
    The client-facing web interface.
    """
    def __init__(self):
        logger.debug("Initializing web engine...")
        self._http_listener = None
        self.listen_port = 5000
        self.listen_addr = '127.0.0.1'
        self.local_base_url = "http://127.0.0.1:%d/" % (self.listen_port,)

    def start(self, ctx=None):
        logger.debug("Starting web engine...")

        self.listen_port = config.agent().getint('webfront', 'listen_port')
        self.listen_addr = config.agent().get('webfront', 'listen_addr')
        self.local_base_url = "http://127.0.0.1:%d/" % (self.listen_port,)

        logger.debug("Local base URL:%s", self.local_base_url)


        ctx.add_child_greenlet(gevent.spawn(self._run))

        logger.debug("Webfront engine started.")

    def stop(self, ctx=None):
        logger.debug("Webfront engine stopped.")

    def _run(self):
        logger.debug("Webfront engine is running...")

        self._http_listener = pywsgi.WSGIServer((self.listen_addr, self.listen_port)
                                                , app)

        logger.debug("Web engine is listening on port: %d", self._http_listener.address[1])

        self._http_listener.serve_forever()
