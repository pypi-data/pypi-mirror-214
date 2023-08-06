#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This file is part of pygal
#
# A python svg graph plotting library
# Copyright © 2012-2014 Kozea
#
# This library is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# This library is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with pygal. If not, see <http://www.gnu.org/licenses/>.


from setuptools import setup, find_packages


with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name="pygal_maps_ua",
    version='1.0.2',
    author="Vadym Holovashchenko",
    description="Ukraine maps for pygal",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="http://github.com/Golova1111/pygal_maps_ua",
    author_email="vadym.holovashchenko@gmail.com",
    license="GNU LGPL v3+",
    platforms="Any",
    packages=find_packages(),
    provides=['pygal_maps_ua'],
    keywords=[
        "svg", "chart", "graph", "maps", "ukraine", "pygal"
    ],
    package_data={'pygal_maps_ua': ['*.Svg']},
    install_requires=["pygal>=1.9.9"],

    entry_points={
        'pygal.maps': [
            'ua = pygal_maps_ua.maps',
        ],
        'pygal.test.test_maps': [
            'ua = pygal_maps_ua.test.test_maps',
        ]
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: "
        "GNU Lesser General Public License v3 or later (LGPLv3+)",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Topic :: Multimedia :: Graphics :: Presentation"
    ]
)