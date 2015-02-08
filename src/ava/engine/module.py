# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
"""
Application module management.
Aa application module provides application-specific functionality.
"""
import os
import sys
import glob
import logging
from ava.runtime import environ

logger = logging.getLogger(__name__)

_MODULES_DIR = 'mods'


class ModuleEngine(object):
    """
    Responsible for managing application modules.
    """

    def __init__(self):
        self.modules = {}
        self.modules_path = os.path.join(environ.home_dir(), _MODULES_DIR, 'enabled')
        self.modules_path = os.path.abspath(self.modules_path)

    def _scan_modules(self):
        pattern = os.path.join(self.modules_path, '[a-zA-Z][a-zA-Z0-9_]*.py')
        return glob.glob(pattern)

    def _import_modules(self, ctx):
        sys.path.append(self.modules_path)

        resource_files = self._scan_modules()

        logger.debug("Found %d module(s)" % len(resource_files))

        for s in resource_files:
            name = os.path.basename(s)
            if '__init__.py' == name:
                continue

            # gets the basename without extension part.
            name = os.path.splitext(name)[0]
            mod = __import__(name)

            self.modules[name] = mod

    def start(self, ctx):
        logger.debug("Starting module engine...")
        self._import_modules(ctx)

    def stop(self, ctx):
        logger.debug("Module engine stopped.")