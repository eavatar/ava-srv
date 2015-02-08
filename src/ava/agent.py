# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import gevent
from gevent import monkey
monkey.patch_all()

import sys
import logging

import importlib

import pkg_resources

from ava import context
from ava.defines import INSTALLED_ENGINES

logger = logging.getLogger(__name__)


def _mygetfilesystemencoding():
    old = sys.getfilesystemencoding

    def inner_func():
        ret = old()
        if ret is None:
            return 'UTF-8'
        else:
            return ret
    return inner_func


def patch_sys_getfilesystemencoding():
    # sys.getfilesystemencoding() always returns None when frozen on Ubuntu systems.
    patched_func = _mygetfilesystemencoding()
    sys.getfilesystemencoding = patched_func


def load_class(full_class_string):
    """
    dynamically load a class from a string. e.g. 'a.b.package:classname'
    """

    class_data = full_class_string.split(":")
    module_path = class_data[0]
    class_name = class_data[1]

    module = importlib.import_module(module_path)
    # Finally, we retrieve the Class
    return class_name, getattr(module, class_name)


class Agent(object):
    def __init__(self):
        logger.debug("Initializing agent...")
        patch_sys_getfilesystemencoding()

        self.running = False
        self.interrupted = False
        self._greenlets = []
        self._context = context.instance(self)
        self._engines = []

    def add_child_greenlet(self, child):
        self._greenlets.append(child)

    def _start_engines(self):
        for it in INSTALLED_ENGINES:
            logger.debug("Loading engine: %s", it)
            name, engine_cls = load_class(it)
            engine = engine_cls()

            self._context.bind(name, engine)
            self._engines.append(self._context[name])

        logger.debug("Starting engines...")
        for it in self._engines:
            it.start(self._context)

    def _stop_engines(self):
        for it in reversed(self._engines):
            it.stop(self._context)

    def context(self):
        return self._context

    def run(self):
        logger.debug("Starting agent...")

        self._start_engines()

        self.running = True
        logger.debug("Agent started.")

        while not self.interrupted:
            try:
                gevent.joinall(self._greenlets, timeout=1)
            except KeyboardInterrupt:
                logger.debug("Interrupted.")
                break

        # stop engines in reverse order.
        self._stop_engines()

        gevent.killall(self._greenlets, timeout=1)

        self.running = False

        logger.debug("Agent stopped.")


def start_agent():
    agent = Agent()
    agent.run()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(name)s - %(message)s')
    start_agent()

