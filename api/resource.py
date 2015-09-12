#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
# Date  : 2015-09-11
# Author: Master Yumi
# Email : yumi@meishixing.com

import json
from api.base import SpuLogging, SpuRequestHandler, Error, Pyobject, PyobjectList, POST
from sputnik.SpuDB import SpuDBManager

mysql_conn = SpuDBManager.get_spudb()

class resource(SpuRequestHandler):
    """
        资源相关接口
    """
    _logging = SpuLogging(module_name="resource", class_name="resource")

    @POST
    def add(self,
            user_id={"atype": int, "adef": 0},
            url={"atype": str, "adef": ""},
            resource_type={"atype": int, "adef": 0},
            latitude={"atype": float, "adef": 0.0},
            longitude={"atype": float, "adef": 0.0},
            create_on={"atype": str, "adef": ""}
    ):
        """
            资源上传
        """
        if user_id == 0 or url == 0:
            return self._response(Pyobject(Error.param_error))

        sql = "insert into resource(user_id,url,resource_type,longitude,latitude,create_on) values(%s,%s,%s,%s,%s,now())" % (
            user_id,
            url, 
            resource_type,
            longitude,
            latitude)
        data = mysql_conn.execsql(sql)
        return self._response(Pyobject(Error.success, data))

    def list(self,
            user_id={"atype": int, "adef": 0},
            resource_type={"atype": int, "adef": 0}
    ):
        """
            获取用户资源信息
        """
        if user_id == 0:
            return self._response(Pyobject(Error.param_error))

        sql = "select * from resource where user_id = %s" % user_id
        if resource_type != 0:
            sql += " and resource_type = %s" %resource_type
        data = mysql_conn.query(sql)

        for i in xrange(0,len(data)):
            data[i]['create_on'] = str(data[i]['create_on'])
        return self._response(Pyobject(Error.success, data))

    def album(self,
              user_id={"atype": int, "adef": ""}
    ):
        self._html_render("resource.html", {})

