# -*- coding: utf-8 -*-
"""
    jaryee.web
    ~~~~~~~~~~~~~~~~~~~

    Jaryee system application

    :copyright: (c) Power by Daqing Chan.
    :license, see LICENSE for more details.
"""


from flask_restful import fields, marshal, reqparse, url_for


# 针对单个表述的LINK
def link_field(endpoint, rel_type='self', absolute=True):

    _link_field = {
        'rel': rel_type,
        'href': fields.Url(endpoint, absolute=absolute)
    }
    return _link_field


# 针对集合表述的LINK
link_fields = {

}

user_detail_fields = {
    'id': fields.Integer,
    'real_name': fields.String,
    'intro': fields.String,
    'add_time': fields.DateTime
}

address_fields = {
    'id': fields.Integer,
    'addr': fields.String,
    'post_code': fields.String,
    'add_time': fields.DateTime
}


user_fields = {
    'id': fields.Integer,
    'email': fields.String,
    'head_ico': fields.String,
    'username': fields.String,
    'role': fields.Integer,
    'password': fields.String,
    'add_time': fields.DateTime,
    'detail': fields.Nested(user_detail_fields),
    'addresses': fields.Nested(address_fields),
}
