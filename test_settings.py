# -*- coding: utf-8 -*-
"""
    jaryee.web
    ~~~~~~~~~~~~~~~~~~~

    Jaryee system application

    :copyright: (c) Power by Daqing Chan.
    :license, see LICENSE for more details.
"""

from datetime import timedelta

DEBUG = True
USE_DIESEL = False
HOST = '0.0.0.0'
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@localhost:3306/restapi?charset=utf8mb4'
SQLALCHEMY_ECHO = False
SQLALCHEMY_POOL_RECYCLE = 20
SECRET_KEY = 'super-secret fuck'
JWT_SECRET_KEY = 'JSON-Web-Token-Projected-Every!!'
JWT_AUTH_URL_RULE = '/api/auth_token'
JWT_EXPIRATION_DELTA = timedelta(seconds=7200)
JWT_LEEWAY = 60