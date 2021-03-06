# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

"""
Imports utility functions from Bottle for exposing web resource.
"""
import os
from ava.util import resource_path

from bottle import route, get, post, delete, put, request, response
from bottle import static_file as _static_file
from ava.core.webfront import dispatcher

static_folder = os.path.join(resource_path('home'), 'static')


def static_file(filepath, root=static_folder, mimetype='auto', download=False, charset='utf-8'):
    return _static_file(filepath, root=root, mimetype=mimetype, download=download, charset=charset)


__all__ = [route, get, post, delete, put, request, response,
           static_file, static_folder, dispatcher, ]

