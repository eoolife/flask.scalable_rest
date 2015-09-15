# !/usr/bin/env python
# -*- coding: utf-8 -*-
# 人生哭短, Python当歌 since 2015


import random

from flask import Flask, request, jsonify, session, redirect, url_for

from flask_scalarest.core.session import FlaskRedisSession

redisSession = FlaskRedisSession()
app = Flask(__name__)
app.config.update(
        DEBUG=True,
        SECRET_KEY='HSDHFSKDFSDFS#$#sdfsdf'
    )
redisSession.init_app(app)

@app.route('/')
def index():
  user_id = session.get('user_id')
  if user_id is not None:
    return """
      Hello. This is index page. Your login is %s.<\br>
      <a href="/logout">Logout</a> <a href="/logout_all_devices">Logout from all devices</a>
    """ % user_id
  else:
    return 'Hello. This is index page. Please <a href="/login">login</a>.'


@app.route('/login')
def login():
  session['user_id'] = random.randint(1, 10000)
  print('login uid %s' % session['user_id'])
  return redirect(url_for('user_info'))


@app.route('/logout')
def logout():
  del session
  return redirect(url_for('index'))


@app.route('/user_info')
def user_info():
    print('====================== user_info =================')
    return jsonify({'name': 'daqing', 'age': 25, 'session_id': session.get('user_id')})


if __name__ == '__main__':
    app.run(debug=True)