# -*- coding: utf-8 -*-

import requests
import random


# curl http://localhost:5000/todos -d "task=something new" -X POST -v
def test_post():
    uri = 'http://localhost:8000/users'
    data = {'id': random.randint(1, 9999999),
            'email': 'd%s%s@d.com' % (random.randint(1, 9999999), random.randint(1, 9999999)),
            'username': '%sdq%s151' % (random.randint(1, 9999999), random.randint(1, 9999999)),
            'password': '123456', 'role': 1,
            'detail.id': random.randint(1, 9999999),
            'detail.real_name': 'ddddd',
            'detail.intro': 'intro',

            'address.id': [random.randint(1, 9999999), random.randint(1, 9999999)],
            'address.post_code': ['527227', '527200'],
            'address.addr': ['sulong taozi', 'luoding']
            }
    import pprint
    pprint.pprint(data)
    resp = requests.post(uri, data=data)
    print resp.status_code


if __name__ == '__main__':
    test_post()