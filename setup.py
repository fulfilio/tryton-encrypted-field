# -*- coding: utf-8 -*-
"""
    setup.py

    :copyright: (c) 2015 by Fulfil.IO Inc.
    :license: see LICENSE for details.
"""
from setuptools import setup

setup(
    name='tryton_encrypted_field',
    version='3.4.0.1',
    description='Encrypted fields in tryton',
    long_description=open('README.rst').read(),
    author="Fulfil.IO Inc.",
    author_email="support@fulfil.io",
    url="https://www.fulfil.io",
    package_dir={'tryton_encrypted_field': '.'},
    packages=[
        'tryton_encrypted_field',
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Plugins',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Office/Business',
    ],
    license='BSD',
    install_requires=[
        "trytond>=3.4,<3.5",
        "cryptography",
    ],
    zip_safe=False,
)
