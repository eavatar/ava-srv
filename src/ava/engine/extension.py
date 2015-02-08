# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from ava.runtime.package import PackageManager
from ava.runtime.extension import ExtensionManager


class ExtensionEngine(object):
    """
    Responsible for managing loading extension packages.
    """
    def __init__(self):
        self._extension_mgr = ExtensionManager()
        self._package_mgr = PackageManager()

    def start(self, ctx):
        self._package_mgr.find_packages()
        self._extension_mgr.load_extensions()
        self._extension_mgr.start_extensions(ctx)

    def stop(self, ctx):
        self._extension_mgr.stop_extensions(ctx)