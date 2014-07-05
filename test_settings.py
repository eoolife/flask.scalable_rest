# -*- coding: utf-8 -*-
"""
    jaryee.web
    ~~~~~~~~~~~~~~~~~~~

    Jaryee system application

    :copyright: (c) Power by Daqing Chan.
    :license, see LICENSE for more details.
"""

DEBUG = True

SQLALCHEMY_DATABASE_URI = 'sqlite:////root/test.db'
SQLALCHEMY_ECHO = DEBUG
SQLALCHEMY_POOL_RECYCLE = 7200