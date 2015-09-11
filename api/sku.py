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
               log={"atype": float, "adef": 0.0},
               distance={"atype": int, "adef": 1000},
    ):
        keyword = keyword.encode("utf8")
        sight_ctrl = top.api.TripScenicSearchRequest()
        sight_ctrl.fields = "product_id, name, pic_url, cid, props, price, tsc"
        sight_ctrl.keywords = keyword
        sight_ctrl.source_point = "120,30"
        sight_ctrl.distance = 100
        data = sight_ctrl.getResponse()
        return self._response(Pyobject(Error.success, data))
