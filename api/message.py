#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
# Date  : 2015-09-11
# Author: Master Yumi
# Email : yumi@meishixing.com

from api.base import SpuLogging, SpuRequestHandler, Error, Pyobject, PyobjectList, POST
from sputnik.SpuDB import SpuDBManager
from config import mongo
from bson.son import SON
from util import calculate_distance

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
            audio_url={"atype": str, "adef":""},
            picture_url={"atype": str, "adef":""},
            category_id={"atype": int,"adef":-1},
            tags={"atype":unicode,"adef":""},
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

        sql = "insert into message(user_id,latitude,longitude,content,audio_url,picture_url,with_sku_id,with_sku_type,create_on,category_id,tags) values(%s,%s,%s,'%s','%s','%s',%s,%s,now(),%s,'%s')" % (
            user_id, 
            latitude,
            longitude,
            content,
            audio_url,
            picture_url,
            with_sku_id,
            with_sku_type,
            category_id,
            tags)
        data = mysql_conn.execsql(sql)
        return self._response(Pyobject(Error.success, data))

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
            sql = "select * from message where id = %s;" % (message_id)
            message_info = mysql_conn.query(sql)
            if not message_info:
                continue
            message_info = message_info[0]
            message_info["create_on"] = str(message_info["create_on"])
            point_user = (longitude, latitude)
            point_message = (message_info["longitude"], message_info["latitude"])
            message_info["distance"] = calculate_distance(point_user, point_message)
            data.append(message_info)
        return self._response(PyobjectList(Error.success, data))

    def list(self,
             user_id={"atype": int, "adef": 0}):
        """获取单个用户的消息列表"""
        sql = "select * from message where user_id = %s;"
        data = mysql_conn.query(sql)
        return self._response(Pyobject(Error.success, data))

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

