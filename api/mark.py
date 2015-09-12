#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
# Date  : 2015-09-11
# Author: Master Yumi
# Email : yumi@meishixing.com

import json
from api.base import SpuLogging, SpuRequestHandler, Error, Pyobject, PyobjectList, POST
from sputnik.SpuDB import SpuDBManager

mysql_conn = SpuDBManager.get_spudb()

class mark(SpuRequestHandler):
    """
        签到相关接口
    """
    _logging = SpuLogging(module_name="mark", class_name="mark")

    @POST
    def add(self,
            user_id={"atype": int, "adef": 0},
            sight_id={"atype": int, "adef": 0},
            longitude={"atype": float, "adef": 0.0},
            latitude={"atype": float, "adef": 0.0}
    ):
        """
            添加签到信息
        """
        if user_id == 0 or sight_id == 0:
            return self._response(Pyobject(Error.param_error))

        sql = "select count(*) total from mark where sight_id = %s" % sight_id
        result = mysql_conn.execsql(sql)
        mark_order = result[0]['total']

        sql = "insert into mark(user_id,sight_id,longitude,latitude,create_on) values(%s,%s,%s,%s,now(),%s)" % (
            user_id, 
            sight_id,
            longitude,
            latitude,
            mark_order)
        data = mysql_conn.execsql(sql)
        return self._response(Pyobject(Error.success, data))

    def get(self,
            user_id={"atype": int, "adef": 0},
    ):
        """
            获取签到信息
        """
        if user_id == 0:
            return self._response(Pyobject(Error.param_error))

        sql = "select * from mark where user_id = %s" % user_id
        data = mysql_conn.query(sql)

        for i in xrange(0,len(data)):
            data[i]['create_on'] = str(data[i]['create_on'])

        return self._response(Pyobject(Error.success, data))
        

