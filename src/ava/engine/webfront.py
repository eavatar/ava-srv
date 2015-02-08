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

logger = logging.getLogger(__name__)


class ApplicationDispatcher(object):
    """Allows one to mount middlewares or applications in a WSGI application.
    """

    def __init__(self, app, mounts=None):
        self.app = app
        self.mounts = mounts or {}

    def __call__(self, environ, start_response):
        script = environ.get('PATH_INFO', '')
        path_info = ''
        while '/' in script:
            if script in self.mounts:
                app = self.mounts[script]
                break
            script, last_item = script.rsplit('/', 1)
            path_info = '/%s%s' % (last_item, path_info)
        else:
            app = self.mounts.get(script, self.app)
        original_script_name = environ.get('SCRIPT_NAME', '')
        environ['SCRIPT_NAME'] = original_script_name + script
        environ['PATH_INFO'] = path_info
        return app(environ, start_response)

    def attach_app(self, path, app):
        self.mounts[path] = app

    def detach_app(self, path):
        app = self.mounts.get(path)
        if app is not None:
            del self.mounts[path]

# the global web application
dispatcher = ApplicationDispatcher(bottle.app())


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
                                                , dispatcher)

        logger.debug("Web engine is listening on port: %d", self._http_listener.address[1])

        self._http_listener.serve_forever()
