#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
# Date  : 2015-09-11
# Author: Master Yumi
# Email : yumi@meishixing.com

import json
from api.base import SpuLogging, SpuRequestHandler, Error, Pyobject, PyobjectList, POST
from sputnik.SpuDB import SpuDBManager

mysql_conn = SpuDBManager.get_spudb()

class pushing(SpuRequestHandler):
    """
        资源相关接口
    """
    _logging = SpuLogging(module_name="pushing", class_name="pushing")

    @POST
    def push(self,
            from_user_id={"atype": int, "adef": 0},
            message_id={"atype": int, "adef": 0}
    ):
        """
            推送message阅读消息
        """
        if from_user_id == 0 or message_id == 0:
            return self._response(Pyobject(Error.param_error))
        sql = "select user_id from message where id = %s" % message_id
        result = mysql_conn.query(sql)
        if len(result) > 0:
            to_user_id = result[0]['user_id']
            sql = "insert into pushing(from_user_id,to_user_id,message_id,enable,create_on) values(%s,%s,%s,%s,now())" % (
                from_user_id,
                to_user_id, 
                message_id,
                1)
            
            data = mysql_conn.execsql(sql)
            return self._response(Pyobject(Error.success, data))
        else:
            return self._response(Pyobject(Error.not_found))

    def get(self,
            user_id={"atype": int, "adef": 0}
    ):
        """
            查询用户是否具有推送
        """
        if user_id == 0:
            return self._response(Pyobject(Error.param_error))

        sql = "select * from pushing where to_user_id = %s and enable = 1" % user_id
        data = mysql_conn.query(sql)

        if len(data) > 0:
            pushed_ids = [str(item.id) for item in data]
            sql = "update pushing set enable = 0 where id in (%s)" % (','.join(pushed_ids))
            mysql_conn.execsql(sql)

            for i in xrange(0,len(data)):
                data[i]['create_on'] = str(data[i]['create_on'])

        return self._response(Pyobject(Error.success, data))
