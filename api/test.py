#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
# Date  : 2015-09-11
# Author: Master Yumi
# Email : yumi@meishixing.com

import json
from api.base import SpuLogging, SpuRequestHandler, Error, Pyobject, PyobjectList

class test(SpuRequestHandler):
    _logging = SpuLogging(module_name="sku", class_name="sku")

    def test(self):
        self._html_render("test.html", {"name": "july"})

