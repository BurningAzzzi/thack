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
            resources={"atype": str, "adef":""},
            routes={"atype":str, "adef":""},
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
        message_obj.with_sku_id = with_sku_id
        message_obj.with_sku_type = with_sku_type
        message_obj.category_id = category_id
        message_obj.tags = tags
        message_id = message_obj.insert()


        resourceIds = resources.split(",")
        for i in xrange(0,len(resourceIds)):
            sql = "insert into message_resources(message_id,resource_id) values(%s,%s)" % (message_id,resourceIds[i])
            mysql_conn.execsql(sql)
        routes = resources.split(",")
        for i in xrange(0,len(routes)):
            sql = "insert into message_routes(message_id,route_id) values(%s,%s)" % (message_id,routes[i])
            mysql_conn.execsql(sql)

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
            message_info["with_sku_id"] = message_obj.with_sku_id
            message_info["with_sku_type"] = message_obj.with_sku_type
            message_info["category_id"] = message_obj.category_id
            message_info["tags"] = message_obj.tags
            message_info["create_on"] = to_utf8(message_obj.create_on)
            message_info["nice"] = message_obj.nice
            point_user = (longitude, latitude)
            point_message = (message_info["longitude"], message_info["latitude"])
            message_info["distance"] = calculate_distance(point_user, point_message)
            data.append(message_info)
        return self._response(PyobjectList(Error.success, data))

    def detail(self,
               id={"atype": int, "adef": 0}
        ):
        if id == 0:
            return self._response(Pyobject(Error.param_error))

        sql = "select * from message where id = %s" % id
        data = mysql_conn.query(sql)
        if len(data) > 0 :
            data[0]['create_on'] = str(data[0]['create_on'])
            
            sql = "select t2.* from message_resources t1 left join resource t2 on t1.resource_id = t2.id where t1.message_id = %s" % id
            message_resources = mysql_conn.query(sql)
            for i in xrange(0,len(message_resources)):
                data[i]['create_on'] = str(message_resources[i]['create_on'])
                
            data[0]['resources'] = message_resources

            sql = "select t2.* from message_routes t1 left join route t2 on t1.route_id = t2.id where t1.message_id = %s" % id
            message_routes = mysql_conn.query(sql)
            for i in xrange(0,len(message_routes)):
                data[i]['create_on'] = str(message_routes[i]['create_on'])
                
            data[0]['routes'] = message_routes
            
            return self._response(PyobjectList(Error.success, data[0]))
        else:
            return self._response(Pyobject(Error.not_found))


    def list(self,
             user_id={"atype": int, "adef": 0}):
        """获取单个用户的消息列表"""
        message_t = MessageModel.table()
        cond = message_t.user_id == user_id
        message_list = MessageModel.objectlist()
        message_list.find(cond)
        return self._response(PyobjectList(Error.success, message_list))

    @POST
    def nice(self,
        id={"atype": int, "adef": 0}
    ):
        """
        点赞
        """
        if id == 0:
            return self._response(Pyobject(Error.param_error))

        sql = "update message set nice = nice + 1 where id = %s" % id
        mysql_conn.execsql(sql)
        return self._response(Pyobject(Error.success))

    def listen(self,
               id={"atype": int, "adef": 0},
    ):
        """
        听
        """
        return self._html_render("listen.html", {
            "id": id,
            })


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

