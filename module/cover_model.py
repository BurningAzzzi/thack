#! /usr/bin/env python
# -*- coding: utf-8 -*-

from sputnik.SpuDBObject import *

class Cover(SpuDBObject):
    _table_ = 'cover'
    def __init__(self, spudb, spucache, debug):
        SpuDBObject.__init__(self, Cover._table_, spudb, spucache, debug = debug)
        self.id = Field(int, 0, 10, auto_inc = True)
        self.name = Field(str, 0, 127)
        self.origin_url = Field(str, '', 150)
        self.url = Field(str, '', 150)
        self.url_md5 = Field(str, '', 32)
        self.description = Field(str, '', 500)
