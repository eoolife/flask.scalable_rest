# -*- coding: utf-8 -*-
"""
    jaryee.web
    ~~~~~~~~~~~~~~~~~~~

    Jaryee system application

    :copyright: (c) Power by Daqing Chan.
    :license, see LICENSE for more details.
"""
import datetime

from ...extensions.database import database
from ...core import DictSerializableMixed


class User(database.Model, DictSerializableMixed):

    __tablename__ = 'tb_user'

    id = database.Column(database.Integer, autoincrement=True, primary_key=True)
    email = database.Column(database.String(100), index=True)
    head_ico = database.Column(database.String(100))
    username = database.Column(database.String(50), index=True)
    role = database.Column(database.SmallInteger, default=0, index=True)    # 0:学生, 1:商家（公司）2:其他
    password = database.Column(database.String(72))
    add_time = database.Column(database.DateTime, default=datetime.datetime.now)

    # relationship follow
    detail = database.relationship('UserDetail', uselist=False, backref=database.backref('user'))
    addresses = database.relationship('Address', backref=database.backref('user'), lazy="dynamic")

    # def to_dict(self):
    #     return dict((c, getattr(self, c)) for c in self.columns)


class UserDetail(database.Model, DictSerializableMixed):

    __tablename__ = 'tb_user_detail'

    id = database.Column(database.Integer, autoincrement=True, primary_key=True)
    real_name = database.Column(database.String(100))
    intro = database.Column(database.String(200))
    add_time = database.Column(database.DateTime, default=datetime.datetime.now)

    user_id = database.Column(database.Integer, database.ForeignKey('tb_user.id'))


class Address(database.Model, DictSerializableMixed):

    __tablename__ = 'tb_address'

    id = database.Column(database.Integer, autoincrement=True, primary_key=True)
    addr = database.Column(database.String(100))
    post_code = database.Column(database.String(10))
    add_time = database.Column(database.DateTime, default=datetime.datetime.now)

    user_id = database.Column(database.Integer, database.ForeignKey('tb_user.id'))