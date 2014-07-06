# -*- coding: utf-8 -*-
"""
    jaryee.web
    ~~~~~~~~~~~~~~~~~~~

    Jaryee system application

    :copyright: (c) Power by Daqing Chan.
    :license, see LICENSE for more details.
"""

DEBUG = True
USE_DIESEL = False
HOST = '0.0.0.0'
SQLALCHEMY_DATABASE_URI = 'sqlite:////test.db'
SQLALCHEMY_ECHO = False
SQLALCHEMY_POOL_RECYCLE = 7200