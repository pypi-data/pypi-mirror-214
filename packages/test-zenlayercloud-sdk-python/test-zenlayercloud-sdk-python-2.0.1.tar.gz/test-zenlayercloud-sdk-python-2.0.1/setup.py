#!/usr/bin/env python

"""
distutils/setuptools install script.
"""
import os

from setuptools import setup, find_packages

import zenlayercloud

ROOT = os.path.dirname(__file__)

setup(
    name='test-zenlayercloud-sdk-python',
    install_requires=["requests>=2.27.0"],
    version=zenlayercloud.__version__,
    description='Test pZenlayer Cloud SDK for Python',
    long_description=open('README.rst').read(),
    author='Zenlayer Cloud',
    url='https://github.com/wolfgangzhu/zenlayercloud-sdk-python',
    maintainer_email="zenlayercloudapi@zenlayer.com",
    scripts=[],
    packages=find_packages(exclude=["tests*"]),
    license="Apache License 2.0",
    platforms='any',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
)
