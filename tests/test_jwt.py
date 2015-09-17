# !/usr/bin/env python
# -*- coding: utf-8 -*-
# 人生哭短, Python当歌 since 2015

import jwt
import json
import requests


if __name__ == '__main__':

    JWT_SECRET_KEY = 'JSON-Web-Token-Projected-Every!!'
    token = 'eyJhbGciOiJIUzI1NiIsImV4cCI6MTQ0MjQ3NTY3NCwiaWF0IjoxNDQyNDY4NDE0fQ.eyJ1c2VyX2lkIjoxfQ.VpTiXb887msGFl95BT70jwkRX4XDUifgmJpo9Zlfp_A'
    decode_data = jwt.decode(token, JWT_SECRET_KEY, algorithms=['HS256'], verify=False)
    print(decode_data)

    session = requests.Session()

    # payload = {'username': 'daqing', 'password': '1234561'}
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
