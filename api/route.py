#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
# Date  : 2015-09-11
# Author: Master Yumi
# Email : yumi@meishixing.com

import json
from api.base import SpuLogging, SpuRequestHandler, Error, Pyobject, PyobjectList, POST
from sputnik.SpuDB import SpuDBManager

mysql_conn = SpuDBManager.get_spudb()

class route(SpuRequestHandler):
    """
        轨迹相关接口
    """
    _logging = SpuLogging(module_name="route", class_name="route")

    @POST
    def add(self,
            user_id={"atype": int, "adef": 0},
            latitude={"atype": float, "adef": 0.0},
            longitude={"atype": float, "adef": 0.0},
            resources={"atype": str, "adef": ""}
    ):
        """
            路线上传
        """
        if user_id == 0:
            return self._response(Pyobject(Error.param_error))

        resourceIds = resources.split(",")
        if len(resourceIds) == 0:
            return self._response(Pyobject(Error.param_error))

        if latitude == 0.0 or longitude == 0.0:
            sql = "select * from resource where id = %s" % resourceIds[0]
            data = mysql_conn.query(sql)
            if len(data) == 0:
                return self._response(Pyobject(Error.param_error))
            else:
                longitude = data[0]['longitude']
                latitude = data[0]['latitude']
        sql = "insert into route(user_id,longitude,latitude,create_on) values(%s,%s,%s,now())" % (
            user_id,
            longitude,
            latitude)
        routeId = mysql_conn.execsql(sql)

        for i in xrange(0,len(resourceIds)):
            sql = "insert into route_resources(route_id,resource_id) values(%s,%s)" % (routeId,resourceIds[i])
            mysql_conn.execsql(sql)
        return self._response(Pyobject(Error.success, routeId))

    def list(self,
            user_id={"atype": int, "adef": 0}
    ):
        """
            获取轨迹信息
        """
        if user_id == 0:
            return self._response(Pyobject(Error.param_error))

        sql = "select * from route where user_id = %s order by id desc" % user_id
        data = mysql_conn.query(sql)
        for i in xrange(0,len(data)):
            data[i]['create_on'] = str(data[i]['create_on'])
        return self._response(Pyobject(Error.success, data))

    def getById(self,
                id={"atype": int,"adef":0}
    ):
        if id == 0:
            return self._response(Pyobject(Error.param_error))

        sql = "select t_rel.resource_id,t_resc.longitude,t_resc.resource_type,t_resc.latitude,t_resc.url,t_resc.create_on from route_resources t_rel left join resource t_resc on t_rel.resource_id = t_resc.id where route_id = %s order by t_resc.create_on" % id
        data = mysql_conn.query(sql)
        for i in xrange(0,len(data)):
            data[i]['create_on'] = str(data[i]['create_on'])
        return self._response(Pyobject(Error.success, data))

    def route_detail(self,
                route_id={"atype": int,"adef":0}
    ):
        sql = "select t_rel.resource_id,t_resc.longitude,t_resc.resource_type,t_resc.latitude,t_resc.url,t_resc.create_on from route_resources t_rel left join resource t_resc on t_rel.resource_id = t_resc.id where route_id = %s order by t_resc.create_on" % route_id
        data = mysql_conn.query(sql)
        for i in xrange(0,len(data)):
            data[i]['create_on'] = str(data[i]['create_on'])
        return self._html_render("route_detail.html", {"resources": data})
