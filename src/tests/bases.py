# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import

import unittest
import itertools
import gevent
import falcon
import falcon.testing
import time
import os
from tempfile import NamedTemporaryFile

from ava.core.agent import Agent
from ava.core.task.asteval import Interpreter


class AgentTest(unittest.TestCase):
    """
    For integration tests with the agent.
    """
    _agent = None

    @classmethod
    def setUpClass(cls):
        AgentTest._agent = Agent()
        server_greenlet = gevent.spawn(AgentTest._agent.run)

        while not AgentTest._agent.running:
            gevent.sleep(0.5)

    @classmethod
    def tearDownClass(cls):
        AgentTest._agent.context().data_engine.remove_all_stores()
        AgentTest._agent.interrupted = True
        while AgentTest._agent.running:
            gevent.sleep(0.5)


