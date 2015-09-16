#!/usr/bin/env python
# -*- coding:utf8 -*-

import os
from appmetrics.wsgi import AppMetricsMiddleware
from flask_scalarest import create_app


here = os.path.dirname(os.path.realpath(__file__))
config_file = os.path.join(here, 'test_settings.py')
application = create_app(config_file)


if __name__ == '__main__':
    application.wsgi_app = AppMetricsMiddleware(application.wsgi_app)
    print(application.url_map)
    application.run(
        host=application.config.get('HOST', '0.0.0.0'),
        port=application.config.get('PORT'),
        debug=application.config['DEBUG'],
    )
