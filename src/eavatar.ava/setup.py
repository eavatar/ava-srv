# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name="eavatar.ava",
    version="0.1.0",
    description="EAvatar Ava - A versatile agent for publishing web resources.",
    # package_dir={'': ''},
    packages=find_packages(exclude=['tests']),
    include_package_data=True,

    # install_requires = ['setuptools'],
    test_suite='nose.collector',
    zip_safe=False,

    entry_points = {
        'console_scripts': [
            'avad = avad:main',
        ],
        'gui_scripts': [
            'avaw = avaw:main',
        ],
    },

    author="Sam Kuo",
    author_email="sam@eavatar.com",
    url="http://www.eavatar.com",

)