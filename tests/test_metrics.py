# !/usr/bin/env python
# -*- coding: utf-8 -*-
# 人生哭短, Python当歌 since 2015

from flask import Flask, jsonify
from appmetrics import metrics

app = Flask(__name__)


@app.route('/factorial/<int:n>')
@metrics.with_meter("factorial-tp")
@metrics.with_histogram("factorial-latency")
@metrics.with_meter("throughput")
def factorial(n):
    f = 1
    for i in xrange(2, n+1):
        f *= i
    return jsonify(factorial=str(f))


@app.route('/is-prime/<int:n>')
@metrics.with_meter("primality-tp")
@metrics.with_histogram("primality-latency")
@metrics.with_meter("throughput")
def is_prime(n):
    result = True

    if n % 2 == 0:
        result = False
    else:
        for i in xrange(3, int(n**0.5)+1, 2):
            if n % i == 0:
                result = False
    return jsonify(is_prime=result)


if __name__ == '__main__':
    from appmetrics.wsgi import AppMetricsMiddleware
    app.wsgi_app = AppMetricsMiddleware(app.wsgi_app)
    app.run(threaded=True, debug=True)