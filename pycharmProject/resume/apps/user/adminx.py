#!/usr/bin/env python
# encoding: utf-8

"""
@version: 1.0
@author: liyao
@license: Apache Licence
@contact: yli@posbao.net
@site: http://www.piowind.com/
@software: PyCharm
@file: adminx.py
@time: 2017/7/4 17:04
"""
import xadmin
from xadmin import views

from user.models import Role, Authority
from .models import VerifyCode

class VerifyCodeAdmin(object):
    list_display = ['code', 'mobile', "add_time"]

class RoleAdmin(object):
    list_display = ['name', 'user','desc', "add_time"]

class AuthorityAdmin(object):
    list_display = ['name', 'role','desc', "add_time"]

xadmin.site.register(Role, RoleAdmin)
xadmin.site.register(Authority, AuthorityAdmin)
xadmin.site.register(VerifyCode, VerifyCodeAdmin)
