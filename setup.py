#!/usr/bin/env python

# Copyright © Michal Čihař <michal@weblate.org>
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""Setup script for customization demo."""

from setuptools import setup, find_packages

setup(
    name='weblate-chatgpt',
    version='0.1.0',
    description='ChatGPT machine translation engine for Weblate',
    author='Dennis',
    author_email='dingxing@xd.com',
    url='https://github.com/your_username/weblate-chatgpt',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'requests',
        'openai'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
