# !/usr/bin/env python
# -*- coding: utf-8 -*-
# 人生哭短, Python当歌 since 2015


from __future__ import  print_function

from passlib.hash import sha256_crypt


hash = sha256_crypt.encrypt("123456")
print(hash)

verify_result = sha256_crypt.verify('123456', hash)
print(verify_result)