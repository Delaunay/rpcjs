#!/usr/bin/env python

from setuptools import setup


if __name__ == '__main__':
    setup(
        name='rpcjs',
        version='0.0.0',
        description='Small Dashboard library',
        author='Pierre Delaunay',
        packages=[
            'rpcjs',
        ],
        setup_requires=['setuptools'],
        tests_require=['pytest', 'flake8', 'codecov', 'pytest-cov'],
    )
