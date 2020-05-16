#!/usr/bin/env python
import os
from setuptools import setup


if __name__ == '__main__':
    _base = os.path.dirname(os.path.realpath(__file__))
    static_path = f'{_base}/rpcjs/static/'

    files = [
        f'{static_path}/bootstrap.darkly.min.css',
        f'{static_path}/bootstrap.min.css',
        f'{static_path}/bootstrap.min.js',
        f'{static_path}/rpcjs.js',
        f'{static_path}/jquery.3.4.1.slim.min.js',
        f'{static_path}/popper.min.js',
        f'{static_path}/socket.io.js',
    ]

    setup(
        name='rpcjs',
        version='0.0.0',
        description='Small Dashboard library',
        author='Pierre Delaunay',
        packages=[
            'rpcjs',
        ],
        data_files=[('rpcjs/static', files)],
        setup_requires=['setuptools'],
        tests_require=[
            'pytest', 'flake8', 'codecov', 'pytest-cov'
        ],
        install_requires=[
            'altair',
            'eventlet',
            'flask',
            'flask-socketio'
        ]
    )
