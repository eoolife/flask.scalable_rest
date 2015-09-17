# -*- coding: utf-8 -*-

import datetime

from flask_restful import Resource, marshal_with, reqparse, abort, url_for, marshal
from flask import request, _request_ctx_stack, redirect

from ...extensions.rest import rest_api
from ...extensions.database import database as db
from ...extensions.jwt import jwt_required
from ...core.metrics import metrics

from .models import (User, UserDetail, Address)

from .fields import user_detail_fields, user_fields, address_fields


def fmt_date(val):
    return val.strftime('%Y-%m-%d %H:%M:%S')


def add_self_atom_link(data, **kwargs):
    atom_link_tag = {'link': {'rel': 'self', 'href': request.url}}
    data.update(atom_link_tag)


class UserResource(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        super(UserResource, self).__init__()

    @staticmethod
    def use_exist(user_id):
        user = User.query.filter(User.id == user_id).first()
        if not user:
            abort(404, message=u'id is %s not exist here' % user_id, error_code=404)
        return user


    @jwt_required()
    @metrics.with_meter("user-get-tp")
    @metrics.with_histogram("user-get-latency")
    @metrics.with_meter("user-throughput")
    @marshal_with(user_fields)
    def get(self, user_id):
        if hasattr(_request_ctx_stack.top, "current_user"):
            current_user = _request_ctx_stack.top.current_user
            # user = self.use_exist(user_id)
            return current_user, 200
        else:
            return redirect('/api/auth_token')

    @metrics.with_meter("user-put-tp")
    @metrics.with_histogram("user-put-latency")
    @metrics.with_meter("user-put-throughput")
    def put(self, user_id):
        user = self.use_exist(user_id)
        return {}, 200

    @metrics.with_meter("user-delete-tp")
    @metrics.with_histogram("user-delete-latency")
    @metrics.with_meter("user-delete-throughput")
    def delete(self, user_id):
        user = self.use_exist(user_id)
        return {}, 200


class UsersResource(Resource):

    def get_reqparse(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('page', type=int, location='args')
        self.reqparse.add_argument('size', type=int, location='args')

    def __init__(self):
        self.reqparse = reqparse.RequestParser()

        self.reqparse.add_argument('id', type=int, required=True, help='entry id must here', location='form')
        self.reqparse.add_argument('email', type=str, required=True, help='email is must here!', location='form')
        self.reqparse.add_argument('head_ico', type=str, location='form')
        self.reqparse.add_argument('username', type=str, required=True, location='form')
        self.reqparse.add_argument('role', type=int, required=True, location='form')
        self.reqparse.add_argument('password', type=str, required=True, location='form')

        self.reqparse.add_argument('detail.id', type=int, location='form')
        self.reqparse.add_argument('detail.real_name', type=str, location='form')
        self.reqparse.add_argument('detail.intro', type=str, location='form')

        self.reqparse.add_argument('address.id', type=int, location='form', action='append')
        self.reqparse.add_argument('address.post_code', type=str, location='form', action='append')
        self.reqparse.add_argument('address.addr', type=str, location='form', action='append')

        super(UsersResource, self).__init__()

    @staticmethod
    def parse_detail(**args):
        detail_args = {}
        for k, v in args.iteritems():
            if k.find('detail') == -1:
                continue
            if k.find('.') == -1:
                continue
            detail_args.update({k.split('.')[1]: v})
        return detail_args

    @metrics.with_meter("users-get-tp")
    @metrics.with_histogram("uses-get-latency")
    @metrics.with_meter("users-get-throughput")
    def get(self):
        self.get_reqparse()

        args = self.reqparse.parse_args()
        page = args['page']
        size = args['size']

        _users = User.query.paginate(page, per_page=size, error_out=False)
        if page > _users.pages:
            abort(400, message="page no can't max than pages, no users data!", error_date=fmt_date(datetime.datetime.now()))
        if not _users.items:
            abort(404, message="no users data!", error_date=fmt_date(datetime.datetime.now()))

        users = {'users': map(lambda t: marshal(t, user_fields), _users.items), 'total': _users.total,
                 'base_url': request.url_root[:-1],
                 'link': {'rel': 'self', 'href': request.url},
                 'previous': url_for('users_ep', page=_users.prev_num, size=size),
                 'next': url_for('users_ep', page=_users.next_num, size=size)}

        if not _users.has_prev:
            users.pop('previous')
        if not _users.has_next:
            users.pop('next')

        return users, 200

    @marshal_with(user_fields)
    def post(self):
        args = self.reqparse.parse_args()

        email = args['email']
        username = args['username']
        user = User.query.filter(db.or_(User.email == email, User.username == username)).first()
        if user:
            return marshal({}, user_fields), 301
        user = User()
        user.id = args['id']
        user.username = username
        user.email = email
        user.head_ico = args['head_ico']
        user.role = args['role']
        user.password = args['password']

        detail_args = self.parse_detail(**args)
        if detail_args:
            user.detail = UserDetail()
            user.detail.id = detail_args['id']
            user.detail.real_name = detail_args['real_name']
            user.detail.intro = detail_args['intro']
        db.session.add(user)
        db.session.commit()
        return {'user': marshal(user.to_dict(), user_fields)}, 201


class AddressResource(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()

        self.reqparse.add_argument('id', type=int, location='form', action='append')
        self.reqparse.add_argument('post_code', type=str, location='form', action='append')
        self.reqparse.add_argument('addr', type=str, location='form', action='append')

        super(AddressResource, self).__init__()

    def get(self, addr_id):
        return {}, 200

    def put(self, addr_id):
        return {}, 200

    def delete(self, addr_id):
        return {}, 200


class AddressListResource(Resource):

    def get_reqparse(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('page', type=int, location='args')
        self.reqparse.add_argument('size', type=int, location='args')

    def __init__(self):
        self.reqparse = reqparse.RequestParser()

        self.reqparse.add_argument('id', type=int, location='form', action='append')
        self.reqparse.add_argument('post_code', type=str, location='form', action='append')
        self.reqparse.add_argument('addr', type=str, location='form', action='append')

        super(AddressListResource, self).__init__()

    def get(self):
        self.get_reqparse()
        return {}, 200

    def post(self):
        return {}, 201


class QrcodeResource(Resource):
    """生产二维码的API"""

    @jwt_required()
    @metrics.with_meter("qrcode-tp")
    @metrics.with_histogram("qrcode-latency")
    @metrics.with_meter("qrcode-throughput")
    def get(self, qrcode_id):
        pass

    @jwt_required()
    @metrics.with_meter("qrcode-tp")
    @metrics.with_histogram("qrcode-latency")
    @metrics.with_meter("qrcode-throughput")
    def put(self, qrcode_id):
        pass

    @jwt_required()
    @metrics.with_meter("qrcode-tp")
    @metrics.with_histogram("qrcode-latency")
    @metrics.with_meter("qrcode-throughput")
    def delete(self, qrcode_id):
        pass


class QrcodeListResource(Resource):

    @jwt_required()
    @metrics.with_meter("qrcode-tp")
    @metrics.with_histogram("qrcode-latency")
    @metrics.with_meter("qrcode-throughput")
    def get(self):
        pass

    @jwt_required()
    @metrics.with_meter("qrcode-tp")
    @metrics.with_histogram("qrcode-latency")
    @metrics.with_meter("qrcode-throughput")
    def post(self):
        pass


rest_api.add_resource(UsersResource,
                      '/users', endpoint='users_ep', methods=['GET', 'POST'])
rest_api.add_resource(UserResource,
                      '/user/<int:user_id>', endpoint='user_ep', methods=['GET', 'DELETE', 'PUT'])

rest_api.add_resource(AddressResource,
                      '/address/<int:addr_id>', endpoint='addr_ep', methods=['GET', 'DELETE', 'PUT'])
rest_api.add_resource(AddressListResource,
                      '/addresses', endpoint='addrs_ep', methods=['GET', 'POST'])

rest_api.add_resource(QrcodeResource, '/qrcode/<qrcode_id>')
rest_api.add_resource(QrcodeListResource, '/qrcodes')