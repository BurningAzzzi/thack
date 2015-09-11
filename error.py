#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
# Date  : 2015-09-11
# Author: Master Yumi
# Email : yumi@meishixing.com

"""

"""

import sys
from config import *
from sputnik.SpuLogging import SpuLogging
from sputnik.SpuError import SpuErrorCodeGen, SpuError
from sputnik.SpuUOM import setdoc

__code_gen = None

def code():
    global __code_gen
    if not __code_gen:
        # 200 -- 1100
        __code_gen = SpuErrorCodeGen(1000)
    return __code_gen.code()

class Error:
    code_dict = {}
    doc_info = ''

    @classmethod
    def load_code_dict(cls, c = '<br>'):
        for e in cls.__dict__:
            v = cls.__dict__[e]
            if type(v) == tuple and type(v[0]) == int and type(v[1]) == str:
                cls.code_dict[v[0]] = v
                # add doc info
                cls.doc_info += "Msg:%s%sCode:%s%sInfo:%s%s" % (e, c, v[0], c, v[1], c*2)

    @classmethod
    def error(cls, code):
        if cls.code_dict.get(code):
            return cls.code_dict[code]
        return (SpuError.unknow_error, '未知错误')


class APIInternalError(Exception):
    def __init__(self, error_msg=''):
        self.error_msg = "API内部错误:'%s'" % error_msg
        SpuLogging.error(self.error_msg)

    def __str__(self):
        return self._msg

Error.success = (code(), '')
Error.unsupport_auth_type = (code(), '不支持该第三方平台')
Error.login_error = (code(), '登录失败')
Error.unlogin = (401, '用户未登录')
Error.param_error = (code(), '参数值或参数类型错误')
Error.order_submit_failure = (code(), '订单提交失败')
Error.not_found = (code(), '未找到匹配数据')

Error.load_code_dict()

info = "Error Info:<br>%s" % Error.doc_info
setdoc(info)
