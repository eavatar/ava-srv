# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

"""
Imports utility functions from Bottle for exposing web resource.
"""

from bottle import route, get, post, delete, put, request, response, static_file


__all__ = [route, get, post, delete, put, request, response, static_file, ]