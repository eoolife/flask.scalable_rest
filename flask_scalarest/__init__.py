#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 人生苦短,我用python
from __future__ import absolute_import

from diesel.web import DieselFlask
from diesel import runtime

from .extensions.database import database
from .extensions.rest import rest_api



BLUEPRINTS = ()


def create_app(config_file):
    app = DieselFlask(__name__)
    runtime.current_app = app.diesel_app
    app.config.from_pyfile(config_file)
    configure_blueprints(app)
    configure_extensions(app)
    init_database(app)

    return app


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


def configure_blueprints(app):
    for blueprint, url_prefix in BLUEPRINTS:
        app.register_blueprint(blueprint, url_prefix=url_prefix)


def configure_extensions(app):
    rest_api.init_app(app)
