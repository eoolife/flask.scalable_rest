#!/usr/bin/env python
# -*- coding:utf8 -*-

import os
from appmetrics.wsgi import AppMetricsMiddleware
from flask_scalarest import create_app
from flask_scalarest.extensions.jwt import jwt


here = os.path.dirname(os.path.realpath(__file__))
config_file = os.path.join(here, 'test_settings.py')
application = create_app(config_file)
application.wsgi_app = AppMetricsMiddleware(application.wsgi_app)
jwt.init_app(application)


if __name__ == '__main__':
    application.run()