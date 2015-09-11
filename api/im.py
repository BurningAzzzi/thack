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
        content = content.encode("utf8")
        if from_user_id == 0 or to_user_id == 0:
            return self._response(Pyobject(Error.param_error))

        sql = "insert into im(from_user_id,to_user_id,content,create_on) values(%s,%s,'%s',now())" % (
            from_user_id, 
            to_user_id,
            content)
        data = mysql_conn.execsql(sql)
        return self._response(Pyobject(Error.success, data))

    def getContacts(self,
                    user_id={"atype":int, "adef": 0}
    ):
        """
            获取最近联系人列表
        """
        if user_id == 0:
            return self._response(Pyobject(Error.param_error))

        sql = "select * from (select to_user_id,user.username to_user_name, max(create_on)create_on,(select content from im temp where temp.from_user_id = %s and temp.to_user_id = main.to_user_id order by id desc limit 1)content from im main left join user on user.id=main.to_user_id where from_user_id = %s group by to_user_id)t order by id desc" % (user_id, user_id)
        data = mysql_conn.query(sql)

        for i in xrange(0,len(data)):
            data[i]['create_on'] = str(data[i]['create_on'])

        return self._response(Pyobject(Error.success, data))

    def getContactContent(self,
                          from_user_id={"atype": int, "adef": 0},
                          to_user_id={"atype": int, "adef": 0},
                          last_id={"atype": int, "adef": 0}
    ):
        """
            获取最新的聊天内容
        """
        if from_user_id == 0 or to_user_id == 0:
            return self._response(Pyobject(Error.param_error))

        sql = "select * from im where ((from_user_id = %s and to_user_id = %s) or (from_user_id = %s and to_user_id = %s))" % (from_user_id,to_user_id,to_user_id,from_user_id)

        if last_id != 0:
            sql += " and id > %s" % last_id

        sql += " order by id desc limit 10"

        data = mysql_conn.query(sql)
        for i in xrange(0,len(data)):
            data[i]['create_on'] = str(data[i]['create_on'])
        return self._response(Pyobject(Error.success, data))

    def index(self,
              from_user_id={"atype": int, "adef": 0},
              to_user_id={"atype": int, "adef": 0}
    ):
        """
            聊天页面
        """
        sql = "select a.username from_user_name,b.username to_user_name from user a,user b where a.id = %s and b.id = %s limit 1" % (from_user_id, to_user_id)

        data = mysql_conn.query(sql)

        output = {}
        if len(data) > 0:
            output['from_user_name'] = data[0]['from_user_name'].encode("utf8")
            output['to_user_name'] = data[0]['from_user_name'].encode("utf8")
            output['from_user_id'] = from_user_id
            output['to_user_id'] = to_user_id

        self._html_render("im.html", output)

