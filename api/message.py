#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
# Date  : 2015-09-11
# Author: Master Yumi
# Email : yumi@meishixing.com

import json
from api.base import SpuLogging, SpuRequestHandler, Error, Pyobject, PyobjectList, POST


class message(SpuRequestHandler):
    _logging = SpuLogging(module_name="message", class_name="message")

    @POST
    def add(self,
            lat={"atype": float, "adef": 0.0},
            lon={"atype": float, "adef": 0.0},
            content={"atype": unicode, "adef": ""},
    ):
        pass
    
