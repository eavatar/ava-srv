# -*- coding: utf-8 -*-
"""
Exceptions raised in eavtar.kits package.
"""
from __future__ import absolute_import, division, print_function, unicode_literals


class EAvatarError(Exception):
    """
    Raised when error is framework-related but no specific error subclass exists.
    """
    def __init__(self, *args, **kwargs):
        super(EAvatarError, self).__init__(args, kwargs)


class DataError(EAvatarError):
    """
    Generic error related to database operations.
    """
    pass


