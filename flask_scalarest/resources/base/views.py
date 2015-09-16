# !/usr/bin/env python
# -*- coding: utf-8 -*-
# 人生哭短, Python当歌 since 2015

import datetime

from flask_restful import Resource, marshal_with, reqparse, abort, url_for, marshal
from flask import request

from ...extensions.rest import rest_api
from ...extensions.database import database as db

from ..example.models import User


class ApiTokenResource(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()

        self.reqparse.add_argument('uid', type=int, required=True, help='user id must here', location='form')
        self.reqparse.add_argument('password', type=str, required=True, help='password is must here!', location='form')

        super(ApiTokenResource, self).__init__()

    def post(self):
        args = self.reqparse.parse_args()

        user_id = int(args['uid'])
        password = str(args['password'])

        user = User.query.filter(User.id == user_id).first()
        if not user:
            abort(404, message=u'用户不存在，请检查用户ID和密码是否正确' % user_id, error_code=404)
        if not user.verify_password(password):
            abort(403, message=u'用户密码错误，请重新授权？至多尝试5次', error_code=403)

        ret = {
            'token': '',
            'uid': user.id,
            'expires': 60 * 60 * 24 # 默认一天
        }

        return ret, 200


