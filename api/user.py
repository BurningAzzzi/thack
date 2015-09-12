#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
# Date  : 2015-09-11
# Author: Master Yumi
# Email : yumi@meishixing.com

import json
from api.base import SpuLogging, SpuRequestHandler, Error, Pyobject, PyobjectList, POST
import top.api
from sputnik.SpuDB import SpuDBManager

mysql_conn = SpuDBManager.get_spudb()

top.setDefaultAppInfo("23012937", "20a702ee2816e5ae3b7f1e637621fcf6")

class user(SpuRequestHandler):
    _logging = SpuLogging(module_name="user", class_name="user")

    @POST
    def login(self,
              username={"atype": str, "adef": ""},
              password={"atype": str, "adef": ""},
    ):
        """
        用户登录
        """
        if username == "" or password == "":
            return self._response(Pyobject(Error.param_error))

        sql = "select id,username,password from user where username = '%s'" % username
        data = mysql_conn.query(sql)
        if len(data) > 0:
            if password == data[0]['password']:
              pass
            else:
              return self._response(Pyobject(Error.password_error))
        else:
            return self._response(Pyobject(Error.user_not_found))

        return self._response(Pyobject(Error.success,data[0]))
        
