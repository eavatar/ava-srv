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

from wsgidav.fs_dav_provider import FilesystemProvider
from wsgidav.wsgidav_app import DEFAULT_CONFIG, WsgiDAVApp
from ava.runtime import environ
from ava.webfront import dispatcher


class WebDavEngine(object):
    """
    The client-facing web interface.
    """
    def __init__(self):
        logger.debug("Initializing webdav engine...")
        self._http_listener = None
        self.listen_port = 5000

    def start(self, ctx=None):
        logger.debug("Starting webdav engine...")

        provider = FilesystemProvider(environ.home_dir())

        conf = DEFAULT_CONFIG.copy()
        conf.update({
            b"mount_path": b'/dav',
            b"provider_mapping": {b"/": provider},
            b"port": 5000,
            b"user_mapping": {},
            b"verbose": 1,
            b"propsmanager": True,
            b"locksmanager": True,
        })

        dav_app = WsgiDAVApp(conf)
        dispatcher.attach_app(b'/dav', dav_app)
        logger.debug("Webdav engine started.")

    def stop(self, ctx=None):
        logger.debug("WebDAV engine stopped.")




