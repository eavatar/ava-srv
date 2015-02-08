# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import logging
import pkg_resources


logger = logging.getLogger(__name__)


class Extension(object):
    def __init__(self, name, entry_point):
        self.name = name
        self.entry_point = entry_point
        self.cls = None
        self.obj = None


class ExtensionManager(object):
    def __init__(self, namespace="eavatar.extension"):
        self.namespace = namespace
        self.extensions = []

    def load_extensions(self, invoke_on_load=True):
        for it in pkg_resources.working_set.iter_entry_points(self.namespace, name=None):
            logger.debug("Loading extension: %s at module: %s", it.name, it.module_name)
            logger.debug("")
            extension = it.load()
            ext = Extension(it.name, it)
            ext.cls = it.load()

            if invoke_on_load:
                ext.obj = ext.cls()
            self.extensions.append(ext)

    def start_extensions(self, context=None):
        for ext in self.extensions:
            startfun = getattr(ext.obj, "start", None)
            if startfun is not None and callable(startfun):
                    startfun(context)

    def stop_extensions(self, context=None):
        for ext in self.extensions:
            stopfun = getattr(ext.obj, "stop", None)
            if stopfun is not None and callable(stopfun):
                try:
                    stopfun(context)
                except Exception:
                    pass
                    #IGNORED.
