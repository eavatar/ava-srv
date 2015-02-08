# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import sys


def create(platform=sys.platform):
    """
    Creates the shell based on a specified platform.

    :param platform: The platform identifier.
    :return:
    """
    if platform.startswith("win32"):
        from ava.shell.wx import Shell
    elif platform.startswith("darwin"):
        from ava.shell.osx import Shell
    elif platform.startswith("linux"):
        from ava.shell.gtk import Shell
    else:
        from ava.shell.console import Shell

    return Shell()