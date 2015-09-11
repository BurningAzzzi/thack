#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
# Date  : 2015-09-11
# Author: Master Yumi
# Email : yumi@meishixing.com

import json
from api.base import SpuLogging, SpuRequestHandler, Error, Pyobject, PyobjectList, POST
from sputnik.SpuDB import SpuDBManager

mysql_conn = SpuDBManager.get_spudb()

class im(SpuRequestHandler):
    """
        签到相关接口
    """
    _logging = SpuLogging(module_name="im", class_name="im")

    @POST
    def add(self,
            from_user_id={"atype": int, "adef": 0},
            to_user_id={"atype": int, "adef": 0},
            content={"atype": unicode, "adef": ""}
    ):
        """
            发送即时通讯消息
        """
        if user_id == 0 or sight_id == 0:
            return self._response(Pyobject(Error.param_error))

        sql = "insert into im(user_id,sight_id,create_on) values(%s,%s,now())" % (
            user_id, 
            sight_id)
        data = mysql_conn.execsql(sql)
        return self._response(Pyobject(Error.success, data))
        

