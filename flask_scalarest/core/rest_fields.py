#!/usr/bin/env python
# -*- coding:utf-8 -*-

from __future__ import absolute_import
from flask_restful import fields, marshal
from flask_restful.fields import Nested, DateTime

from email.utils import formatdate
from calendar import timegm


def rfc822(dt):
    return formatdate(timegm(dt.timetuple()))


# class NestedField(fields.Raw):
#     def __init__(self, nested, **kwargs):
#         self.nested = nested
#         super(NestedField, self).__init__(**kwargs)
#
#     def output(self, key, obj):
#         value = fields.get_value(key if self.attribute is None else self.attribute, obj)
#         return marshal(value, self.nested)
class DateField(fields.Raw):
    """Return a RFC822-formatted date string in UTC"""
    def format(self, value):
        try:
            return rfc822(value)
        except AttributeError as ae:
            raise fields.MarshallingException(ae)
