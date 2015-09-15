# !/usr/bin/env python
# -*- coding: utf-8 -*-
# 人生哭短, Python当歌 since 2015
"""
flask redis session
~~~~~~~~~~~~~~~~~~~

:license: MIT, see LICENSE for more details.
:Date: Sep, 2015
:written by internet

https://github.com/EricQAQ/Flask-RedisSession/blob/master/flask_redisSession/__init__.py

"""
from __future__ import print_function

import json
from datetime import datetime, timedelta
from uuid import uuid4
from redis import Redis
from werkzeug.datastructures import CallbackDict
from flask.sessions import SessionInterface, SessionMixin, total_seconds
from werkzeug.local import Local
import dateutil.parser
from itsdangerous import Signer, BadSignature

local = Local()
SESSION_KEY_PREFIX = 'fsession#'

def _sync_user_sessions(redis, prefix, user_id):
    user_key = _get_user_prefix(user_id)
    sessions = redis.hgetall(user_key)

    be_del_sids = []

    for sid, value in sessions.iteritems():
        sid = sid.decode()
        value = json.loads(value.decode())
        expires = value['expires']
        expires = dateutil.parser.parser(expires)

        if expires < datetime.now():
            be_del_sids.append(sid)
        else:
            session = redis.get("".join([prefix, sid]))
            if session:
                session = json.loads(session.decode())
                if user_id != session['user_id']:
                    be_del_sids.append(sid)
    if len(be_del_sids) > 0:
        redis.hdel(user_key, *be_del_sids)

def _get_user_prefix(user_id):
    return "user_sessions:%s" % user_id


class FlaskRedisSession(object):

    def __init__(self, app=None):
        if app is not None:
            self.app = app
            self.init_app(app)
        else:
            self.app = None

    def init_app(self, app):
        config = app.config
        config.setdefault('SESSION_KEY_PREFIX', SESSION_KEY_PREFIX)
        config.setdefault('REDIS_SESSION', None)
        config.setdefault('USE_SECRET_KEY', True)
        config.setdefault('SESSION_REFRESH_EACH_REQUEST', True)

        # following config is just for the app do not have redis instance
        config.setdefault('REDIS_HOST', 'localhost')
        config.setdefault('REDIS_PORT', 6379)
        config.setdefault('REDIS_DB', 0)
        config.setdefault('REDIS_PASSWORD', None)
        config.setdefault('USE_REDIS_CONNECTION_POOL', False)   # use the connection pool or not
        config.setdefault('MAX_CONNECTION', None)   # the max number of connections.Valid when using connection pool

        app.session_interface = RedisSessionInterface(
            config['REDIS_SESSION'], config['USE_SECRET_KEY'],
            config['SESSION_KEY_PREFIX'], config['USE_REDIS_CONNECTION_POOL'],
            config['PERMANENT_SESSION_LIFETIME'], config['REDIS_HOST'],
            config['REDIS_PORT'], config['REDIS_DB'],
            config['REDIS_PASSWORD'], config['MAX_CONNECTION']
        )


class RedisSession(CallbackDict, SessionMixin):

    def __init__(self, initial=None, session_id=None):
        def on_update(self):
            self.modified = True
        CallbackDict.__init__(self, initial, on_update)
        self.modified = True
        self.permanent = True
        self.session_id = session_id


class ServerSessionMixin(object):

    def generate_sessionid(self):
        return str(uuid4())


class RedisSessionInterface(SessionInterface, ServerSessionMixin):
    serializer = json
    session_class = RedisSession

    def __init__(self, redis, use_sign, session_prefix, use_redis_connection_pool,
                 expire_time, redis_host, redis_port, redis_db, redis_pw, max_conn=None):
        if redis is None:
            from redis import StrictRedis
            if use_redis_connection_pool:
                from redis import ConnectionPool
                pool = ConnectionPool(host=redis_host, port=redis_port,
                                      db=redis_db, max_connections=max_conn)
                redis = StrictRedis(connection_pool=pool)
            else:
                redis = StrictRedis(host=redis_host, port=redis_port,
                                    db=redis_db, password=redis_pw)
        self.redis = redis
        self.use_sign = use_sign
        self.session_prefix = session_prefix
        self.expire_time = expire_time

    def open_session(self, app, request):
        session_id = request.cookies.get(app.session_cookie_name, None)

        if not session_id:
            session_id = self.generate_sessionid()
            return self.session_class(session_id=session_id)

        if self.use_sign and app.secret_key:
            singer = Signer(app.secret_key, salt='fredis-session', key_derivation='hmac')
            try:
                session_id = singer.unsign(session_id).decode('utf-8')
            except BadSignature:
                session_id = None

        data = self.redis.get(self.session_prefix + session_id)
        if data is None:
            return self.session_class(session_id=session_id)
        try:
            json_data = self.serializer.loads(data)
            return self.session_class(json_data, session_id=session_id)
        except:
            return self.session_class(session_id=session_id)

    def save_session(self, app, session, response):
        domain = self.get_cookie_domain(app)
        path = self.get_cookie_path(app)
        if not session and session.modified:
            self.redis.delete(self.session_prefix + session.session_id)
            response.delete_cookie(app.session_cookie_name, domain=domain, path=path)
            return

        httponly = self.get_cookie_httponly(app)
        secure = self.get_cookie_secure(app)
        expire = self.get_expiration_time(app, session)
        serialize_session = self.serializer.dumps(dict(session))

        pipe = self.redis.pipeline()
        pipe.set(self.session_prefix + session.session_id, serialize_session)
        pipe.expire(self.session_prefix + session.session_id, total_seconds(self.expire_time))
        pipe.execute()

        if self.use_sign:
            session_id = Signer(app.secret_key, salt='fredis-session', key_derivation='hmac')\
                            .sign(session.session_id.encode('utf-8'))
        else:
            session_id = session.session_id
            print('session_id: %s' % session_id)

        response.set_cookie(key=app.session_cookie_name, value=session_id,
                            max_age=self.expire_time, expires=expire,
                            path=path, domain=domain,
                            secure=secure, httponly=httponly)
