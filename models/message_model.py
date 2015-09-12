# /usr/bin/env python
# -*- coding: utf-8 -*-
# Author:yinyu
# E-mail:yinyu@meishixing.com
# Date  : 2014-09-18

"""
    图片的模型数据库映射
"""

from sputnik.SpuDB import *
from sputnik.SpuDBObject import *

class MessageModel(SpuDBObject):
    """
        图片公共模型
    """
    _table_ = "message"
    def __init__(self,spudb,spucache,debug):
        SpuDBObject.__init__(self, MessageModel._table_,spudb,spucache,debug=debug)
        # id主键
        self.id = Field(int,0,10,auto_inc = True,primarykey = True)
        self.user_id = Field(int, 0, 10)
        self.latitude = Field(float, 0, 10)
        self.longitude = Field(float, 0, 10)
        self.content = Field(str, '', 256)
        self.with_sku_id = Field(int, 0, 10)
        self.with_sku_type = Field(int, 0, 10)
        self.category_id = Field(int, 0, 10)
        self.tags = Field(str, '', 255)
        self.nice = Field(int, 0)
        self.create_on = Field(datetime, SpuDateTime.current_time())
