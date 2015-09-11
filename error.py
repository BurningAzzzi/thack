#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © meishixing.com
# Date  : 2013-06-05
# Author: niusmallnan
# Email : <zhangzhibo521@gmail.com>
#
# Distributed under terms of the MIT license.

"""

"""

import sys
from config import *
from sputnik.SpuLogging import SpuLogging
from sputnik.SpuError import SpuErrorCodeGen, SpuError
from sputnik.SpuUOM import setdoc
from module.module_error import ModuleError

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
Error.register_duplicate = (code(), '重复注册')
Error.register_failure = (code(), '注册失败')
Error.duplicate_bind_push = (code(), '重复绑定推送token')
Error.fav_operation_failure = (code(), '收藏操作失败')
Error.cancel_order_failure = (code(), '取消订单失败')
Error.invalid_idcard = (code(), '无效的身份证件号')
Error.login_already = (code(), '该用户已登录')
Error.user_not_exist = (code(), '用户不存在')
Error.user_pwd_error = (code(), '用户密码错误')
Error.auth_access_failed = (code(), '访问第三方平台失败')
Error.order_detail_failure = (code(), '订单详情页错误')
Error.ticket_sell_out = (code(), '门票已被抢完')
Error.geting_ticket = (code(), '出票中')
Error.cancelling_ticket = (code(), '取消订单中')
Error.upload_image_failure = (code(), '上传图片失败')
Error.location_error = (code(), '定位失败')
Error.ticket_not_exists = (code(), '票型不存在')
Error.send_phone_verify_err = (code(), '发送验证码到手机失败')
Error.reset_password_failed = (code(), '更新密码失败')
Error.record_not_exist = (code(), '找不到有关的记录')
Error.leo_not_exist = (code(), 'leo不存在')
Error.auth_problem_user = (code(), '账号异常')
Error.api_internal_error = (code(), 'api内部错误,')
Error.action_failure = (code(), '操作失败')
Error.encrypta_modified_exc = (code(), '参数值或参数类型错误')
Error.encrypta_dec_error = (code(), '参数值或参数类型错误')
Error.encrypta_gen_fails = (code(), '生成加密数据失败')
Error.encrypta_enc_error = (code(), '参数值或参数类型错误')
Error.call_baade_error = (code(), '请求Baade出错')
Error.encrypta_error = (code(), "加密或解密错误")
Error.invalid_params = (code(), "无效的参数")
Error.call_rongcloud_error = (code(), '请求rongcloud出错')
Error.add_user_custom = (code(), '添加需求错误')
Error.update_user_custom = (code(), '更新需求错误')
Error.get_user_custom = (code(), '获取需求错误')
Error.get_user_customs = (code(), '获取需求列表错误')
Error.delete_user_custom = (code(), '获取需求列表错误')
Error.session_param_error = (code(), 'session参数错误')
Error.get_session_list = (code(), '获取会话列表错误')
Error.set_isread = (code(), '设置会话已读错误')
Error.get_user_info = (code(), '获取用户信息错误')
Error.call_search_error = (code(), '请求searchengine出错')
Error.nopermission = (code(), "没有权限")

Error.load_code_dict()

info = "Error Info:<br>%s" % Error.doc_info
setdoc(info)
