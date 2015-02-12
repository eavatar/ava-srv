#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
The module acts as the launcher for EAvatar to run in a GUI environment like Windows, OS X or GTK.
"""

from __future__ import print_function, absolute_import

import os
import sys
import logging
import argparse
import pkg_resources
import multiprocessing

#makes multiprocessing work when in freeze mode.
multiprocessing.freeze_support()

# imports dependencies for PyInstaller to figure out what to include.
import depends
# prevent IDE regarding depends as not used.
depends.absolute_import


# imports platform-specific dependencies.
if sys.platform.startswith('darwin'):
    import gui_osx
elif sys.platform.startswith('linux'):
    import gui_linux
elif sys.platform.startswith('win32'):
    import gui_win32


def package_in_path(pkg):
    for path in sys.path:
        if pkg in path:
            return True
    return False


def main():
    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(name)s - %(message)s', level=logging.DEBUG, disable_existing_loggers=False)
    logger = logging.getLogger('avaw')

    entry_name = 'factory'
    if os.environ.get('AVA_NOGUI') is not None:
        entry_name = 'console'

    # add packages in 'eggs' to sys.path in case PyInstaller haven't done that.
    if hasattr(sys, "_MEIPASS") and not package_in_path('eavatar.core'):
        logger.debug("'eggs' not in path, try to add them.")
        eggs_dir = os.path.join(sys._MEIPASS, 'eggs')
        logger.debug("Core packages path: %s", eggs_dir)
        distributions, errors = pkg_resources.working_set.find_plugins(
            pkg_resources.Environment([eggs_dir])
        )

        for it in distributions:
            logger.debug("Added package: %s", it.project_name)
            pkg_resources.working_set.add(it)

        if len(errors) > 0:
            logger.error("failed to load package(s): %s", errors)

    from ava.shell import factory

    logger.debug("Starting the shell...")
    shell = factory.create()
    shell.do_run()
    logger.debug("Shell stopped.")

if __name__ == '__main__':
#    sys.argv.append('--nogui')
    main()