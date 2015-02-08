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

app = bottle.app()

_RESOURCES_DIR = 'resources'


class WebEngine(object):
    def __init__(self):
        logger.debug("Initializing web engine...")
        self._http_listener = None
        self.listen_port = 5000
        self.listen_addr = '127.0.0.1'
        self.local_base_url = "http://127.0.0.1:%d/" % (self.listen_port,)

        self.resources_path = os.path.join(environ.home_dir(), _RESOURCES_DIR, 'enabled')
        self.resources_path = os.path.abspath(self.resources_path)
        self.resources = {}

    def _scan_resources(self):
        pattern = os.path.join(self.resources_path, '[a-zA-Z][a-zA-Z0-9_]*.py')
        return glob.glob(pattern)

    def _bind_web_resources(self, ctx):
        sys.path.append(self.resources_path)

        resource_files = self._scan_resources()

        logger.debug("Found %d resources" % len(resource_files))

        for s in resource_files:
            name = os.path.basename(s)
            if '__init__.py' == name:
                continue

            # gets the basename without extension part.
            name = os.path.splitext(name)[0]
            mod = __import__(name)

            self.resources[name] = mod

    def start(self, ctx=None):
        logger.debug("Starting web engine...")

        self.listen_port = config.agent().getint('web', 'listen_port')
        self.listen_addr = config.agent().get('web', 'listen_addr')
        self.local_base_url = "http://127.0.0.1:%d/" % (self.listen_port,)

        logger.debug("Local base URL:%s", self.local_base_url)


        self._bind_web_resources(ctx)

        ctx.add_child_greenlet(gevent.spawn(self._run))

        logger.debug("Web engine started.")

    def stop(self, ctx=None):
        logger.debug("Web engine stopped.")

    def _run(self):
        logger.debug("Web engine is running...")

        self._http_listener = pywsgi.WSGIServer((self.listen_addr, self.listen_port)
                                                , app)

        logger.debug("Web engine is listening on port: %d", self._http_listener.address[1])

        self._http_listener.serve_forever()


if __name__ == '__main__':
    we = WebEngine()
    we.start()