# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import logging

import pkg_resources

from ava.runtime import environ, config


logger = logging.getLogger(__name__)


class PackageManager(object):
    def __init__(self, pkgs_dir=environ.pkgs_dir()):
        self.pkgs_dir = pkgs_dir

    def find_packages(self, add_to_path=True):
        """
        Extends sys.path at runtime to include distributions in user's home directory.
        """

        #logger.debug("sys.path(before): ", sys.path)


        logger.debug("Packages Directory: %s", self.pkgs_dir)
        distributions, errors = pkg_resources.working_set.find_plugins(
            pkg_resources.Environment([self.pkgs_dir])
        )

        if len(distributions) > 0:
            logger.debug("Found %d extension package(s).", len(distributions))
            #map(pkg_resources.working_set.add, distributions)  # add plugins+libs to sys.path

            if not add_to_path:
                return

            for it in distributions:
                enable_it = False
                if config.packages().has_option("enabled", it.project_name):
                    enable_it = config.packages().getboolean("enabled", it.project_name)
                else:
                    config.packages().set("enabled", it.project_name, 'false')

                if enable_it:
                    pkg_resources.working_set.add(it)
                    logger.debug("package added: %s", it.project_name)
                else:
                    logger.debug("Package found but not added: %s", it.project_name)

            logger.error("Couldn't load: %r", errors)        # display errors
        else:
            logger.debug("No extension package found.")

