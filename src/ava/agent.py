# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import gevent
from gevent import monkey
monkey.patch_all()

import sys
import logging

from ava.engine.extension import ExtensionEngine
from ava.engine.data import DataEngine
from ava.engine.web import WebEngine

from ava import context

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
        ext_engine = ExtensionEngine()
        self._engines.append(ext_engine)
        self._context.bind("ext_engine", ext_engine)

        data_engine = DataEngine()
        self._engines.append(data_engine)
        self._context.bind("data_engine", data_engine)

        web_engine = WebEngine()
        self._engines.append(web_engine)
        self._context.bind("web_engine", web_engine)

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

