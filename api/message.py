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
            user_id={"atype": int, "adef": 0},
            latitude={"atype": float, "adef": 0.0},
            longitude={"atype": float, "adef": 0.0},
            content={"atype": unicode, "adef": ""},
            audio_url={"atype": str, "adef":""},
            image_url={"atype": str, "adef":""},
            with_sku_id={"atype": int, "adef": 0},
            with_sku_type={"atype": int, "adef": 0}
    ):
        content = content.encode("utf8")

        return self._response(Pyobject(Error.param_error))
    
