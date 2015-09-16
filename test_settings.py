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
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@localhost:3316/restapi?charset=utf8mb4'
SQLALCHEMY_ECHO = False
SQLALCHEMY_POOL_RECYCLE = 7200
SECRET_KEY = 'super-secret fuck'