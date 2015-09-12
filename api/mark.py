#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
# Date  : 2015-09-11
# Author: Master Yumi
# Email : yumi@meishixing.com

import json
from api.base import SpuLogging, SpuRequestHandler, Error, Pyobject, PyobjectList, POST
from sputnik.SpuDB import SpuDBManager
from util import to_utf8
import top.api

top.setDefaultAppInfo("23012937", "20a702ee2816e5ae3b7f1e637621fcf6")

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
        result = mysql_conn.query(sql)
        mark_order = result[0]['total']

        sql = "insert into mark(user_id,sight_id,longitude,latitude,create_on,mark_order) values(%s,%s,%s,%s,now(),%s)" % (
            user_id, 
            sight_id,
            longitude,
            latitude,
            mark_order+1)
        id = -1
        try:
            id = mysql_conn.execsql(sql)
        except Exception, e:
            pass
        else:
            pass
        finally:
            pass
        return self._response(Pyobject(Error.success, id))

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
        
    def viewer(self,
               user_id={"atype": int, "adef": 0},
    ):
        """总体情况"""
        sql = "select * from mark where user_id = %s" % user_id
        data = mysql_conn.query(sql)
        sight_ctrl = top.api.TripScenicGetRequest()
        for i in xrange(0,len(data)):
            data[i]['create_on'] = str(data[i]['create_on'])
            data[i]["mark_time"] = "时间:" + data[i]["create_on"]
            sight_id = data[i]["sight_id"]
            sight_ctrl.scenic_id = sight_id
            res = sight_ctrl.getResponse()
            sight_name = res["trip_scenic_get_response"]["travel_scenic"]["name"]
            data[i]["address"] = to_utf8(sight_name)
        return self._html_render("viewer.html", {"markers": data, "user_id": user_id})

