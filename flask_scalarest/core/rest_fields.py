#!/usr/bin/env python
# -*- coding:utf-8 -*-

from __future__ import absolute_import

from flask_restful import fields
from email.utils import formatdate
from calendar import timegm


def rfc822(dt):
    return formatdate(timegm(dt.timetuple()))


class DateField(fields.Raw):
    """Return a RFC822-formatted date string in UTC"""
    def format(self, value):
        try:
            return rfc822(value)
        except AttributeError as ae:
            raise fields.MarshallingException(ae)
