# !/usr/bin/env python
# -*- coding: utf-8 -*-
# 人生哭短, Python当歌 since 2015


from __future__ import  print_function
import random
from passlib.hash import sha256_crypt

password = '123456'
salt = ''.join(random.sample('1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz!@#$%^&*()', 8))
print(salt)
encrypt_str = '%s%s' % (password, salt)
password = sha256_crypt.encrypt(encrypt_str)
hash = sha256_crypt.encrypt(encrypt_str)
print(hash)

verify_result = sha256_crypt.verify(encrypt_str, hash)
print(verify_result)