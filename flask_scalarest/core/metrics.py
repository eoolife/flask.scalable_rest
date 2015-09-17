# !/usr/bin/env python
# -*- coding: utf-8 -*-
# 人生哭短, Python当歌 since 2015

from appmetrics import metrics, reporter
import pprint


def stdout_report(_metrics):
    pprint.pprint(_metrics)


# reporter.register(stdout_report, reporter.fixed_interval_scheduler(20))