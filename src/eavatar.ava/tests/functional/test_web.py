# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import unittest
import requests


class ApiTest(unittest.TestCase):

    def setUp(self):
        self.base_url = 'http://127.0.0.1:5000'

    #### Root resource ####
    def test_get_root_resource(self):
        r = requests.get(self.base_url)
        self.assertEqual(r.status_code, 200)

