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


class Address(database.Model, DictSerializableMixed):

    __tablename__ = 'tb_address'

    id = database.Column(database.Integer, autoincrement=True, primary_key=True)
    addr = database.Column(database.String(100))
    post_code = database.Column(database.String(10))
    add_time = database.Column(database.DateTime, default=datetime.datetime.now)

    user_id = database.Column(database.Integer, database.ForeignKey('tb_user.id'))