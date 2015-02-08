# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from bottle import route, static_file
from ava.util import resource_path

static_folder = resource_path('home/static')


@route('/')
@route('/index.html')
def serve_root():
    return static_file(b'index.html', root=static_folder)


@route('/favicon.ico')
def serve_favicon():
    return static_file(b'favicon.ico', root=static_folder)


@route('/static/<filepath:path>')
def serve_static(filepath):
    return static_file(filepath, root=static_folder)

