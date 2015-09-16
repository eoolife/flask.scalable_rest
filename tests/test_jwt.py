# !/usr/bin/env python
# -*- coding: utf-8 -*-
# 人生哭短, Python当歌 since 2015

import os
import json
import requests


if __name__ == '__main__':

    session = requests.Session()

    payload = {'username': 'daqing', 'password': '123456'}
    headers = {'content-type': 'application/json'}
    response = session.post('http://127.0.0.1:5000/auth',
                             data=json.dumps(payload),
                            headers={'content-type': 'application/json'})
    print response.status_code
    print response.json()

    hello_resp = session.get('http://127.0.0.1:5000/user/1', headers={"Authorization": "Bearer %s" % response.json()['token'] })
    print hello_resp.status_code
    print hello_resp.content
    print hello_resp.headers
