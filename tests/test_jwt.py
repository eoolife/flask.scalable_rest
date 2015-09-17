# !/usr/bin/env python
# -*- coding: utf-8 -*-
# 人生哭短, Python当歌 since 2015

import jwt
import json
import requests


if __name__ == '__main__':

    JWT_SECRET_KEY = 'JSON-Web-Token-Projected-Every!!'
    token = 'eyJhbGciOiJIUzI1NiIsImV4cCI6MTQ0MjQ1NDc3NiwiaWF0IjoxNDQyNDU0Njk2fQ.eyJ1c2VyX2lkIjoxfQ.hdGgzNu2O4IHJIeUkFq_MXDm-Hagt41DheBvF7pdLBw'
    decode_data = jwt.decode(token, JWT_SECRET_KEY, algorithms=['HS256'], verify=False)
    print(decode_data)

    session = requests.Session()

    # payload = {'username': 'daqing', 'password': '123456'}
    # headers = {'content-type': 'application/json'}
    # response = session.post('http://127.0.0.1:5000/api/auth_token',
    #                          data=json.dumps(payload),
    #                         headers={'content-type': 'application/json'})
    # print(response.status_code)
    # print(response.json())

    hello_resp = session.get('http://127.0.0.1:5000/user/1', headers={"Authorization": "Bearer %s" % token })
    print(hello_resp.status_code)
    print(hello_resp.content)
    print(hello_resp.headers)
