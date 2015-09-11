#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © meishixing.com
# Date  : 2014-08-04
# Author: Master Yumi
# 夜空中最亮的星很不错
# Distributed under terms of the MIT license.

"""
    支付部分的api
"""

import sys, xmltodict
sys.path.insert(0, '')
from base import *
from tornado.escape import xhtml_escape as escape
import json, urllib

def to_utf8(text):
    if isinstance(text, unicode):
        return text.encode("utf8")
    return str(text)

class order(SpuRequestHandler):
    """
        订单api
    """
    _logging = SpuLogging(module_name='order', class_name='order')

    def comment(
            self,
            session_id={'adef': '', 'atype': str},
            comment_status={"adef": 0, "atype": int},
            page={'adef': 1, 'atype': int},
            page_size={"adef": 10, "atype": int},
    ):
        data = {"page_total": 0, "pagenumber": 1, "orders": []}
        is_login, user_id = check_login(session_id)
        if not is_login:
            return self._response(Pyobject(Error.success, data))
        try:
            # 获取未评论的接口
            if comment_status == 1:
                result = trans_client.getUnCommentOrderList(user_id=user_id, page=page, page_size=page_size)
                data = json.loads(result.rst)
        except Exception as e:
            self._logging.error("trans_client.getUnCommentOrderList() session_id: %s, page: %s, exception: %s." % (session_id, str(page), str(e)))
            return self._response(Pyobject(Error.api_internal_error, str(e)))
        if result.errno:
            return self._response(Pyobject((result.errno, result.msg)))
        for order in data["orders"]:
            order["leo_id"] = encrypt(str(int(order.get("leo_id", 0))), version=0)[1]
        return self._response(Pyobject(Error.success, data))

    def list(
            self,
            session_id={'adef': '', 'atype': str},
            user_id={"adef": 0, "atype": int},
            biz_id={"adef": 0, "atype": int},
            page={'adef': 1, 'atype': int},
            v={"adef": 1, "atype": int},
            finished={"adef": -1, "atype": int},
            page_size={"adef": 10, "atype": int},
            ):
        """
            获取用户的订单列表
            * session_id : session_id
        """
        if not user_id:
            is_login, user_id = check_login(session_id)
        if not user_id:
            return self._response(Pyobject(Error.unlogin))
        try:
            result = trans_client.getOrderList(user_id, biz_id, {}, page, page_size, finished=finished)
        except Exception as e:
            self._logging.error("trans_client.getOrderList() session_id: %s, page: %s, exception: %s." % (session_id, str(page), str(e)))
            return self._response(Pyobject(Error.api_internal_error, str(e)))
        if result.errno:
            return self._response(Pyobject((result.errno, result.msg)))
        result = json.loads(result.rst)
        if v == 1:
            # 一切为了兼容啊
            for order in result:
                if order["status"] == 5:
                    order["status"] = 2
                if order["status"] == 6:
                    order["status"] = 2
                    
        data = SList()
        data.list(result)
        for d in data:
            d["leo_id"] = encrypt(str(int(d.get("leo_id", 0))), version=0)[1]
            d["map_icon"] = mapicon_ctrl.get_mapicon(d["category_id"])
        return self._response(Pyobject(Error.success, data))

    @POST
    def create(
            self,
            session_id={'adef': '', 'atype': str},
            phone={'adef': '', 'atype': str},
            sku_id={'adef': 0, 'atype': int},
            quantity={'adef': 1, 'atype': int},
            pay_method={'adef': 0, 'atype': int},
            pay_type={"adef": 1, "atype": int},
            order_type={"adef": 1, "atype": int},
            **kwargs):
        """
            创建订单
            order_type 1: 懒人周末app产生的订单 3: wap产生的订单。前端调用的时候不需要传，只有wap需要传
            pay_method: 1: wap支付 2:支付宝钱包 3:微信app支付 4:微信wap支付
            pay_type: 1: 立即支付(在线支付，创建完订单以后直接请求支付url) 2: 景点到付(创建完订单返回订单号，不请求支付url)
            如果是周边游则kwargs传
            c_name : 联系人名字
            c_sex : 联系人性别
            date_info : 日期安排，格式类似这样：[{"relatedId": 159422, "date": "2014-09-20 00:00:00.0000"} , {"relatedId": 159421, "date": "2014-09-20 00:00:00.0000"}]
            p_cert_no : 联系人身份证
            如果是景点则kwargs传
            travel_date: 游玩日期,格式1991-11-11 00:00:00
            other_guest: [{"g_mobile": "13371051285", "g_name": "\u5434\u743c", "id_card": "370705197501029510"}] 如果不是要求实名制的景点，id_card也可以不填。
        """
        order_ip = str(self.tornado.request.remote_ip)
        if order_ip == "::1":
            order_ip = "127.0.0.1"
        user_id = kwargs.get("user_id", 0)
        if not user_id:
            is_login, user_id = check_login(session_id)
        if not user_id:
            return self._response(Pyobject(Error.unlogin))
        result = trans_client.createOrder(session_id, user_id, phone, sku_id, quantity, pay_method=pay_method, order_ip=order_ip, order_type=order_type, **kwargs)

        if result.errno:
            return self._response(Pyobject((result.errno, result.msg)))

        data = SDict()
        data["serial_id"] = result.rst
        data["msg"] = result.msg
        if data["serial_id"] and pay_type == 1:
            r = trans_client.getPayUrl(pay_method=pay_method, serial_id=result.rst, client_ip=order_ip)
            data["url"] = r.rst
        return self._response(Pyobject(Error.success, data))

    def detail(
            self,
            serial_id={'adef': '', 'atype': str},
            v={"adef": 1, "atype": int},
            ):
        """
            获取订单详情
        """
        try:
            detail = trans_client.getOrderDetail(serial_id=serial_id)
        except Exception as e:
            return self._response(Pyobject(Error.api_internal_error, str(e)))
        
        if detail.errno:
            return self._response(Pyobject((detail.errno, detail.msg)))

        detail = json.loads(detail.rst)

        if v == 1:
            # 为了做兼容
            if detail.get("status", 0) == 5:
                detail["status"] = 2
            if detail.get("status", 0) == 6:
                detail["status"] = 2    
 
        data = SDict()
        data.dict(detail)
        data["leo_id"] = encrypt(str(data.get("leo_id", 0)), version=0)[1]
        data["map_icon"] = mapicon_ctrl.get_mapicon(data["category_id"])
        return self._response(Pyobject(Error.success, data))


    @POST
    def cancel(
            self,
            session_id={'adef': '', 'atype': str},
            serial_id={'adef': '', 'atype': str}
            ):
        """
            取消订单
        """
        try:
            result = trans_client.cancelOrder(serial_id)
        except:
            return self._response(Pyobject(Error.api_internal_error))
        data = SDict()
        data["result"] = result.rst
        data["msg"] = result.msg
        return self._response(Pyobject(Error.success, data))

    def pay(
            self,
            session_id={'adef': '', 'atype': str},
            pay_method={'adef': 0, 'atype': int},
            serial_id={'atype': str, 'adef': ''},
            ):
        """
            支付接口,
            pay_method = 1:wap, 2: 支付宝钱包，3: 微信app支付 4:微信wap支付
        """
        client_ip = str(self.tornado.request.remote_ip)
        if client_ip == "::1":
            client_ip = "127.0.0.1"
        try:
            result = trans_client.getPayUrl(pay_method=pay_method, serial_id=serial_id, client_ip=client_ip)
        except:
            return self._response(Pyobject(Error.api_internal_error))
        data = SDict()
        data["url"] = result.rst
        data["msg"] = result.msg
        return self._response(Pyobject(Error.success, data))

    @POST
    def alipay_wap_callback(
            self,
    ):
        """支付宝的回调 out_trade_no是商家唯一订单号"""
        provider = 1
        notify_data = to_utf8(self.tornado.request.body)
        self._logging.info(notify_data)
        try:
            rst = trans_client.on_pay_callback(provider=provider, notify_data=notify_data)
            if rst.errno == 0:
                self.tornado.write("success")
            else:
                self._logging.error(rst.msg)
        except Exception as e:
            self._logging.error(e)

    @POST
    def weixin_pay_callback(
            self,
            # **kwargs
    ):
        """微信支付回调接口"""
        provider = 3
        notify_data = to_utf8(self.tornado.request.body)
        self._logging.info(notify_data)
        try:
            rst = trans_client.on_pay_callback(provider=provider, notify_data=notify_data)
            if rst.errno == 0:
                response_body = "<xml><return_code><![CDATA[SUCCESS]]></return_code><return_msg><![CDATA[OK]]></return_msg></xml>"
                self.tornado.write(response_body)
            else:
                self._logging.error(rst.msg)
        except Exception as e:
            self._logging.error(e)

    @POST
    def weixin_wap_pay_callback(
            self,
            # **kwargs
    ):
        """微信支付回调接口"""
        provider = 3
        notify_data = to_utf8(self.tornado.request.body)
        self._logging.info(notify_data)
        try:
            rst = trans_client.on_pay_callback(provider=provider, notify_data=notify_data)
            if rst.errno == 0:
                response_body = "<xml><return_code><![CDATA[SUCCESS]]></return_code><return_msg><![CDATA[OK]]></return_msg></xml>"
                self.tornado.write(response_body)
            else:
                self._logging.error(rst.msg)
        except Exception as e:
            self._logging.error(e)

    @POST
    def alipay_package_callback(
            self,
            # notify_id={"adef": "", "atype": str},
            # out_trade_no={"adef": "", "atype": str},
            # buyer_email={'adef': "", 'atype': str},
            # trade_status={"adef": "", "atype": str},
            # refund_status={"adef": "", "atype": str},
            # **kwargs
    ):
        """支付宝的回调 out_trade_no是商家唯一订单号"""
        provider = 2
        notify_data = to_utf8(self.tornado.request.body)
        self._logging.info(notify_data)
        try:
            rst = trans_client.on_pay_callback(provider=provider, notify_data=notify_data)
            if rst.errno == 0:
                self.tornado.write("success")
            else:
                self._logging.error(rst.msg)
        except Exception as e:
            self._logging.error(e)

    @POST
    def pay_callback(
            self,
            serial_id={'adef': '', 'atype':str}):
        """
            同城回调
        """
        provider = 4
        notify_data = to_utf8(self.tornado.request.body)
        self._logging.info(notify_data)
        try:
            rst = trans_client.on_pay_callback(provider=provider, notify_data=notify_data)
            if rst.errno == 0:
                self.tornado.write(rst.rst)
            else:
                self._logging.error(rst.msg)
        except Exception as e:
            self._logging.error(e)

    def tc_callback(
            self,
            serial_id={'adef': '', 'atype':str}):
        """
            同程景点回调
        """
        provider = 5
        notify_data = to_utf8(self.tornado.request.body)
        self._logging.info(notify_data)
        try:
            rst = trans_client.on_pay_callback(provider=provider, notify_data=notify_data)
            if rst.errno == 0:
                self.tornado.write(rst.rst)
            else:
                self._logging.error(rst.msg)
        except Exception as e:
            self._logging.error(e)


class tailor(SpuRequestHandler):
    _logging = SpuLogging(module_name="order", class_name="tailor")
    
    @POST
    def create(
            self,
            session_id={'adef': '', 'atype': str},
            phone={'adef': '', 'atype': str},
            custom_id={'adef': 0, 'atype': int},
            quantity={'adef': 1, 'atype': int},
            pay_method={'adef': 0, 'atype': int},
            contacter_name={"adef": "", "atype": unicode},
            pay_type={"adef": 1, "atype": int}):
        """
            创建订单
            如果是周边游则kwargs传
            c_name : 联系人名字
            c_sex : 联系人性别
            date_info : 日期安排，格式类似这样：[{"relatedId": 159422, "date": "2014-09-20 00:00:00.0000"} , {"relatedId": 159421, "date": "2014-09-20 00:00:00.0000"}]
            p_cert_no : 联系人身份证
            pay_method: 1: wap支付 2:支付宝钱包
        """
        contacter_name = contacter_name.encode("utf8")
        order_ip = str(self.tornado.request.remote_ip)
        is_login, user_id = check_login(session_id)
        if not user_id:
            return self._response(Pyobject(Error.unlogin))
        result = trans_client.createTailorOrder(session_id, user_id, phone, custom_id, quantity, pay_method=pay_method, order_ip=order_ip, contacter_name=contacter_name)

        if result.errno:
            return self._response(Pyobject((result.errno, result.msg)))

        data = SDict()
        data["serial_id"] = result.rst
        data["msg"] = result.msg
        if data["serial_id"] and pay_type == 1:
            r = trans_client.getPayUrl(pay_method=pay_method, serial_id=result.rst, client_ip=order_ip)
            data["url"] = r.rst
        return self._response(Pyobject(Error.success, data))
    
            
if __name__ == '__main__':
    trans_client.say()


