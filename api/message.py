#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
# Date  : 2015-09-11
# Author: Master Yumi
# Email : yumi@meishixing.com

import json
from api.base import SpuLogging, SpuRequestHandler, Error, Pyobject, PyobjectList, POST
from sputnik.SpuDB import SpuDBManager

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
        user_id={"atype": int, "adef": 0},
        latitude={"atype": float, "adef": 0},
        longitude={"atype": float, "adef": 0},
        category_id={"atype": int, "adef": 0}
    ):
        """
            查找消息
        """
        sql = "select * from message where 1=1 "
        if user_id != 0:
            sql += ("and user_id = %s" % user_id)
        if latitude != 0 and longitude != 0:
            # 地理位置匹配
            pass
        if category_id != 0:
            sql += ("and category_id = %s" % category_id)

        data = mysql_conn.query(sql)
        for i in xrange(0,len(data)):
            data[i]['create_on'] = str(data[i]['create_on']);

        return self._response(Pyobject(Error.success, data))        

class sku_type(SpuRequestHandler):
    _logging = SpuLogging(module_name="message", class_name="type")

    def get(self):
        sql = "select * from sku_type"
        return self._response(Pyobject(Error.success, data))

    def getById(self,
        id={"atype":int,"adef":0}
    ):
        if id == 0:
            return self._response(Pyobject(Error.param_error))

        sql = "select * from sku_type where id = %s" % id
        data = mysql_conn.query(sql)
        if len(data) > 0:
            return self._response(Pyobject(Error.success, data[0]))
        else:
            return self._response(Pyobject(Error.not_found))     

class category(SpuRequestHandler):
    _logging = SpuLogging(module_name="message", class_name="category")

    def get(self):
        sql = "select * from category"
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

