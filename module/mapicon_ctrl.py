#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
# Date  : 2015-05-13
# Author: Master Yumi
# Email : yumi@meishixing.com

"""
    不想写warehouse，就先放在这里吧
"""


from sputnik.SpuDBObject import *

map_icon = {
    1: {1: "http://image.mibang.meishixing.com/leo/client/20150513172710_hotel.png"},
    2: {2: "http://image.mibang.meishixing.com/leo/client/20150513172711_ticket.png"},
    3: {2: "http://image.mibang.meishixing.com/leo/client/20150513172711_ticket.png", 1: "http://image.mibang.meishixing.com/leo/client/20150513172710_hotel.png"},
    4: {4: ""},
    5: {5: "http://image.mibang.meishixing.com/leo/client/20150513172710_bar.png"},
    6: {6: "http://image.mibang.meishixing.com/leo/client/20150513172711_music.png"},
    7: {7: "http://image.mibang.meishixing.com/leo/client/20150513172711_stage.png"},
    8: {8 :"http://image.mibang.meishixing.com/leo/client/20150513172711_pic.png"},
    9: {9: "http://image.mibang.meishixing.com/leo/client/20150513172710_food.png"},
    10: {10: "http://image.mibang.meishixing.com/leo/client/20150513172710_bag.png"},
    11: {11: "http://image.mibang.meishixing.com/leo/client/20150513172711_movie.png"},
    12: {12: "http://image.mibang.meishixing.com/leo/client/20150513172711_persons.png"},
    13: {13:"http://image.mibang.meishixing.com/leo/client/20150513172710_basketball.png"},
    14: {14: "http://image.mibang.meishixing.com/leo/client/20150513172710_leaf.png"},
    15: {15: "http://image.mibang.meishixing.com/leo/client/20150513172711_shirt.png"},
    16: {16: ""},
    17: {17: "http://image.mibang.meishixing.com/leo/client/20150513172711_ticket.png"},
    18: {18: "http://image.mibang.meishixing.com/leo/client/20150819140714_tailor.png"},
}

Detail_Category_Icon = {
    3: 'http://image.mibang.meishixing.com/leo/img/20150630095215_95bce957b873b0e9adc771a9f52e432a.png',
    5: 'http://image.mibang.meishixing.com/leo/img/20150630095057_9d0068dce2c033d01640fa1cac1c6662.png',
    6: 'http://image.mibang.meishixing.com/leo/img/20150630095410_15f5e5ae1850845ce3198a92440e9690.png',
    7: 'http://image.mibang.meishixing.com/leo/img/20150630095306_c2897d2c581f8db03592d5f565c79e30.png',
    8: 'http://image.mibang.meishixing.com/leo/img/20150630095446_d406416e55492afb299a8a7da3f5b9b1.png',
    9: 'http://image.mibang.meishixing.com/leo/img/20150630095329_43c91c36bc679ac499e4b28e5184a8ba.png',
    10: 'http://image.mibang.meishixing.com/leo/img/20150630094916_573a3993a43a402a8fb3c30a61750014.png',
    11: 'http://image.mibang.meishixing.com/leo/img/20150630095349_6eec12c621de6ab8946671593e831ae2.png',
    12: 'http://image.mibang.meishixing.com/leo/img/20150630095427_c03f97363a4f49562bb1f43bd3171c6d.png',
    13: 'http://image.mibang.meishixing.com/leo/img/20150630095129_ab07326a4419494433cd461978754b3a.png',
    14: 'http://image.mibang.meishixing.com/leo/img/20150630095149_041685046565dfc5f56837093e19e9a3.png',
    15: 'http://image.mibang.meishixing.com/leo/img/20150630095245_a0b1fde06f91e7db1c80439fc2d43376.png',
    18: 'http://image.mibang.meishixing.com/leo/client/20150819140714_tailor.png',
}

class MapIconCtrl(object):
    _logging = SpuLogging(module_name="mapicon_ctrl", class_name="MapIcon")

    def __init__(self):
        pass

    def get_mapicon(self, category_id):
        if map_icon.has_key(int(category_id)):
            return map_icon.get(int(category_id), {})
        self._logging.error("Cant find mapicon for category_id : %s" % category_id)
        return {}

    def getDetailCategoryIcon(self, category_id):
        return Detail_Category_Icon.get(category_id, '')
