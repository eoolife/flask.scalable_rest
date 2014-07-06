# -*- coding: utf-8 -*-
"""
    jaryee.web
    ~~~~~~~~~~~~~~~~~~~

    Jaryee system application

    :copyright: (c) Power by Daqing Chan.
    :license, see LICENSE for more details.
"""
from collections import OrderedDict


class DictSerializableMixed(object):

    def to_dict(self):
        result = OrderedDict()
        for key in self.__mapper__.c.keys():
            val = getattr(self, key)
            result[key] = val
            # if isinstance(val, datetime.datetime):
            #     result[key] = val.strftime('%Y-%m-%d %H:%M:%S')
            # else:
            #     result[key] = val
        return result