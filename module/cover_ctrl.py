#! /usr/bin/env python
# -*- coding: utf-8 -*-

import time
from sputnik.SpuDateTime import SpuDateTime
from sputnik.SpuBase import SpuBase
from sputnik.SpuDBObject import *
from cover_model import Cover
import hashlib

class CoverCtrl(object):
    _logging = SpuLogging(module_name='cover_ctrl', class_name='CoverCtrl')

    def __init__(self):
        pass

    def insert_to_db(self, name, url, origin_url='', description=''):
        """
            insert the cover into db
        """
        table = Cover.table()
        table_name = table.name
        cover = Cover.object()
        cover.name = name
        cover.origin_url = origin_url
        cover.url = url
        url_md5 = hashlib.md5(url).hexdigest()
        cover.url_md5 = url_md5
        cover.description = description
        try:
            last_id = cover.insert()
            if last_id == -2:
                self._logging.error("duplicate occurs while inserting table:'%s', data:'%s'" % (table_name, url))
                return False
        except Exception, e:
            self._logging.error("Exception occurs while inserting table:'%s', data:'%s'" % (table_name,  url))
            return False
        return True

    def update_to_db(self, id, name, url, origin_url='', description=''):
        """
            insert the cover into db
        """
        table = Cover.table()
        table_name = table.name
        cover = Cover.object()
        cover.id = id
        cover.name = name
        cover.origin_url = origin_url
        cover.url = url
        url_md5 = hashlib.md5(url).hexdigest()
        cover.url_md5 = url_md5
        cover.description = description
        try:
            last_id = cover.update()
            if last_id == -2:
                self._logging.error("duplicate occurs while inserting table:'%s', data:'%s'" % (table_name, (id, url)))
                return False
        except Exception, e:
            self._logging.error("Exception occurs while inserting table:'%s', data:'%s'" % (table_name, (id, url)))
            return False
        return True

    def get(self, id):
        """
            get the cover from db
        """
        cover_t = Cover.table()
        cover_list = Cover.objectlist()
        cond = SqlNone()
        if id:
            if id == 0:
                cond = cond 
            else:
                cond = cond & (cover_t.id == id)
        cover_list.find(cond)
        return cover_list

    