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
            if hasattr(val, 'isoformat') and callable(val.isoformat):
                result[key] = val.isoformat()
            else:
                result[key] = val
        return result