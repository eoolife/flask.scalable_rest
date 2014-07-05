# -*- coding: utf-8 -*-
"""
    jaryee.web
    ~~~~~~~~~~~~~~~~~~~

    Jaryee system application

    :copyright: (c) Power by Daqing Chan.
    :license, see LICENSE for more details.
"""
from flask_restful import Resource, marshal_with, marshal

from ...extensions.rest import rest_api
from .models import (User, UserDetail, Address)


class UserResource(Resource):

    #@marshal_with()
    pass


class UsersResource(Resource):

    pass


rest_api.add_resource(UsersResource, '/users', methods=['GET', 'POST'])
rest_api.add_resource(UserResource, '/user/<int:user_id>', methods=['GET', 'DELETE', 'PUT'])