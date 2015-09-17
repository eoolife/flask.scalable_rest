#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 人生苦短,我用python

from __future__ import absolute_import, print_function
from flask import Flask

from .extensions.database import database
from .extensions.rest import rest_api

from .resources.example import (UserResource, UsersResource)
from .resources.base import (ApiTokenResource,)


def create_app(config_file, use_diesel=False):
    app = Flask(__name__)
    app.config.from_pyfile(config_file)
    configure_extensions(app)
    init_database(app)
    configure_resource(app)
    return app


def configure_resource(app):

    print('Restful API LIST FINISHED!')


def configure_sqlalchemy_log(app):
    import logging
    logging.basicConfig()
    level = logging.ERROR
    if app.config['DEBUG']:
        level = logging.INFO
    logging.getLogger('sqlalchemy.engine').setLevel(level)


def init_database(app):
    database.init_app(app)
    database.create_all()


def configure_extensions(app):
    rest_api.init_app(app)
    rest_api.app = app


def configure_errors(app):
    errors = {
        'UserAlreadyExistsError': {
            'message': "A user with that username already exists.",
            'status': 409,
        },
        'ResourceDoesNotExist': {
            'message': "A resource with that ID no longer exists.",
            'status': 410,
            'extra': "Any extra information you want.",
        },
    }

