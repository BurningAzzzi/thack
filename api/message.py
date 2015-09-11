#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
# Date  : 2015-09-11
# Author: Master Yumi
# Email : yumi@meishixing.com

from api.base import SpuLogging, SpuRequestHandler, Error, Pyobject, PyobjectList, POST
from sputnik.SpuDB import SpuDBManager
from config import mongo
from bson.son import SON
from util import calculate_distance, to_utf8
from models.message_model import MessageModel

mysql_conn = SpuDBManager.get_spudb()

class message(SpuRequestHandler):
    """
        “说”消息相关接口
    """
    _logging = SpuLogging(module_name="message", class_name="message")

    @POST
    def add(self,
            user_id={"atype": int, "adef": 0},
            latitude={"atype": float, "adef": 0.0},
            longitude={"atype": float, "adef": 0.0},
            content={"atype": unicode, "adef": ""},
            audio_url={"atype": str, "adef": ""},
            picture_url={"atype": str, "adef": ""},
            category_id={"atype": int,"adef": 0},
            tags={"atype":unicode,"adef": ""},
            with_sku_id={"atype": int, "adef": 0},
            with_sku_type={"atype": int, "adef": 0}
    ):
        """
            添加一条消息
        """
        content = content.encode("utf8")
        tags = tags.encode("utf8")
        if user_id == 0 or latitude == 0 or longitude == 0:
            return self._response(Pyobject(Error.param_error))
        message_obj = MessageModel.object()
        message_obj.user_id = user_id
        message_obj.latitude = latitude
        message_obj.longitude = longitude
        message_obj.content = content
        message_obj.audio_url = audio_url
        message_obj.picture_url = picture_url
        message_obj.with_sku_id = with_sku_id
        message_obj.with_sku_type = with_sku_type
        message_obj.category_id = category_id
        message_obj.tags = tags
        message_id = message_obj.insert()
        # 插入mongodb
        mongo.message.insert({"id": int(message_id), "loc": [longitude, latitude], "category_id": category_id})
        return self._response(Pyobject(Error.success, message_id))

    def search(self,
               latitude={"atype": float, "adef": 0},
               longitude={"atype": float, "adef": 0},
               category_id={"atype": int, "adef": 0},
               distance={"atype": int, "adef": 1000},
    ):
        """
            查找消息
        """
        cond = {}
        if category_id:
            cond["category_id"] = category_id
        message_list = mongo.message.find({"loc": SON([("$near", [longitude, latitude]), ("$maxDistance", distance)])})
        data = []
        for message in message_list:
            message_id = message["id"]
            message_t = MessageModel.table()
            message_obj = MessageModel.object()
            cond = message_t.id == message_id
            if not message_obj.find(cond):
                continue
            message_info = {}
            message_info["id"] = message_obj.id
            message_info["user_id"] = message_obj.user_id
            message_info["latitude"] = message_obj.latitude
            message_info["longitude"] = message_obj.longitude
            message_info["content"] = message_obj.content
            message_info["audio_url"] = message_obj.audio_url
            message_info["picture_url"] = message_obj.picture_url
            message_info["with_sku_id"] = message_obj.with_sku_id
            message_info["with_sku_type"] = message_obj.with_sku_type
            message_info["category_id"] = message_obj.category_id
            message_info["tags"] = message_obj.tags
            message_info["create_on"] = to_utf8(message_obj.create_on)
            point_user = (longitude, latitude)
            point_message = (message_info["longitude"], message_info["latitude"])
            message_info["distance"] = calculate_distance(point_user, point_message)
            data.append(message_info)
        return self._response(PyobjectList(Error.success, data))

    def list(self,
             user_id={"atype": int, "adef": 0}):
        """获取单个用户的消息列表"""
        message_t = MessageModel.table()
        cond = message_t.user_id == user_id
        message_list = MessageModel.objectlist()
        message_list.find(cond)
        return self._response(PyobjectList(Error.success, message_list))

class sku_type(SpuRequestHandler):
    _logging = SpuLogging(module_name="message", class_name="type")

    def get(self):
        sql = "select * from sku_type"
        data = mysql_conn.query(sql)
        return self._response(Pyobject(Error.success, data))

    def getById(self,
                sku_id={"atype":int,"adef":0}
    ):
        if sku_id == 0:
            return self._response(Pyobject(Error.param_error))

        sql = "select * from sku_type where id = %s" % sku_id
        data = mysql_conn.query(sql)
        if len(data) > 0:
            return self._response(Pyobject(Error.success, data[0]))
        else:
            return self._response(Pyobject(Error.not_found))     

class category(SpuRequestHandler):
    _logging = SpuLogging(module_name="message", class_name="category")

    def get(self):
        sql = "select * from category"
        data = mysql_conn.query(sql)
        return self._response(Pyobject(Error.success, data))

    def getById(self,
        id={"atype":int,"adef":0}
    ):
        if id == 0:
            return self._response(Pyobject(Error.param_error))

        sql = "select * from category where id = %s" % id
        data = mysql_conn.query(sql)
        if len(data) > 0:
            return self._response(Pyobject(Error.success, data[0]))
        else:
            return self._response(Pyobject(Error.not_found))            

