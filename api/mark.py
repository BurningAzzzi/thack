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
    ):
        """
            添加签到信息
        """
        if user_id == 0 or sight_id == 0:
            return self._response(Pyobject(Error.param_error))

        sql = "insert into mark(user_id,sight_id,create_on) values(%s,%s,now())" % (
            user_id, 
            sight_id)
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
        return self._response(Pyobject(Error.success, data))
        

