# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import os
import sys
import glob
import logging
import gevent
import bottle
from gevent import pywsgi
from wsgidav.version import __version__
from ava.runtime import config
from ava.runtime import environ

logger = logging.getLogger(__name__)


class ApplicationDispatcher(object):
    """Allows one to mount middlewares or applications in a WSGI application.
    """

    def __init__(self, app, mounts=None):
        self.app = app
        self.mounts = mounts or {}

    def __call__(self, environ, start_response):
        script = environ.get(b'PATH_INFO', b'')
        path_info = ''
        while b'/' in script:
            if script in self.mounts:
                app = self.mounts[script]
                break
            script, last_item = script.rsplit(b'/', 1)
            path_info = b'/%s%s' % (last_item, path_info)
        else:
            app = self.mounts.get(script, self.app)
        original_script_name = environ.get(b'SCRIPT_NAME', b'')
        environ[b'SCRIPT_NAME'] = original_script_name + script
        environ[b'PATH_INFO'] = path_info
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
        logger.debug("Initializing webfront engine...")
        self._http_listener = None
        self.listen_port = 5000
        self.listen_addr = '127.0.0.1'
        self.local_base_url = "http://127.0.0.1:%d/" % (self.listen_port,)

    def start(self, ctx=None):
        logger.debug("Starting webfront engine...")

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

        conf_dir = environ.conf_dir()
        keyfile = os.path.join(conf_dir, 'ava.key')
        certfile = os.path.join(conf_dir, 'ava.crt')

        self._http_listener = pywsgi.WSGIServer((self.listen_addr, self.listen_port),
                                                dispatcher,
                                                keyfile=keyfile,
                                                certfile=certfile)

        self._http_listener.set_environ({b"SERVER_SOFTWARE": b"WsgiDAV/{} ".format(__version__) +
                                           self._http_listener.base_env["SERVER_SOFTWARE"]})
        logger.debug("Webfront engine is listening on port: %d", self._http_listener.address[1])

        self._http_listener.serve_forever()
