# !/usr/bin/env python
# -*- coding: utf-8 -*-
# 人生哭短, Python当歌 since 2015


import jwt


def jwt_decode(token, secret=None, algorithms=None, verify=False):
    """
        对经过JWT（JSON Web Token）Hash的token进行对称加密出明文
        :param token: token, jwtencode之后的
        :param secret: 需要加入hash的密钥
        :param algorithms: hash算法
        :param verify: 验证
    """
    decode_data = jwt.decode(token, secret, algorithms=algorithms or ['HS256'], verify=verify)
    return decode_data