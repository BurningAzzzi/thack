#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
# Date  : 2015-09-11
# Author: Master Yumi
# Email : yumi@meishixing.com

import json
from api.base import SpuLogging, SpuRequestHandler, Error, Pyobject, PyobjectList
import top.api

top.setDefaultAppInfo("23012937", "20a702ee2816e5ae3b7f1e637621fcf6")

class sku(SpuRequestHandler):
    _logging = SpuLogging(module_name="sku", class_name="sku")

    def search(self,
               keyword={"atype": unicode, "adef": ""},
               lat={"atype": float, "adef": 0.0},
               lon={"atype": float, "adef": 0.0},
               distance={"atype": int, "adef": 10},
               page={"atype": int, "adef": 1},
    ):
        keyword = keyword.encode("utf8")
        sight_ctrl = top.api.TripScenicSearchRequest()
        sight_ctrl.fields = "product_id, name, pic_url, cid, props, price, tsc"
        sight_ctrl.keywords = keyword
        sight_ctrl.source_point = "%s,%s" % (lon, lat)
        sight_ctrl.distance = distance
        sight_ctrl.current_page = page
        data = sight_ctrl.getResponse()
        data = data["trip_scenic_search_response"]["scenic_result"]
        if data.has_key("condition_list"):
            data.pop("condition_list")
        for d in data["scenic_list"]["travel_scenic"]:
            scenic_pics = d["scenic_pics"]
            pics = [url for url in scenic_pics.split(',') if url.strip()]
            d["scenic_pics"] = pics
        return self._response(Pyobject(Error.success, data))

class sight(SpuRequestHandler):
    _logging = SpuLogging(module_name="sku", class_name="sight")

    def detail(self,
               scenic_id={"adef": 0, "atype": int}):
        sight_ctrl = top.api.TripScenicGetRequest()
        sight_ctrl.scenic_id = scenic_id
        data = sight_ctrl.getResponse()
        return self._response(Pyobject(Error.success, data))
        
