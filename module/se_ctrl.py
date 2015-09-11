#! /usr/bin/env python
# -*- coding: utf-8 -*-
# ht <515563130@qq.com, weixin:jacoolee>

import json

from sputnik.SpuLogging import SpuLogging
from sputnik.SpuPythonObject import SDict, SList, STuple

from se.client.SearchEngine.ttypes import *
from se.client.se_client import SearchEngineClient
from se.client.se_formula import *

from base_ctrl import SE_RPC_ADDRESS


SpuLogging.info("\tRPC search engine address:%s,\t port:%s" % (SE_RPC_ADDRESS[0], SE_RPC_ADDRESS[1]))
seclient = SearchEngineClient()
seclient.connect(SE_RPC_ADDRESS[0], SE_RPC_ADDRESS[1])


class SearchEngineCtrl(object):
    _logging = SpuLogging(module_name='se_ctrl', class_name='SearchEngineCtrl')
    # why use macro instead of 1 directly?
    # Caz using number directly is much more bug-potential.
    _ORDER_MACRO = [            # 'MACRO' -> index
        ''                      # 0
        , 'LOCATION'            # 1
        , 'CREATE_TIME'         # 2
        , 'UPDATE_TIME'         # 3
        , 'END_TIME'            # 4
    ]

    _ORDER_MAP = { str(i[0]):i[1] for i in enumerate(_ORDER_MACRO) }

    def __init__(self, ):
        pass

    def _sorder_desc2macro(self, sorder_desc):
        """
        @sorder_desc: a string description of sort order, it's ordered and seperated by ':'
        """
        self._logging.info("raw sort order description:'%s'"% sorder_desc)
        if not sorder_desc or not isinstance(sorder_desc, str):
            self._logging.warn("sorder_desc is '%s', type:'%s'" % (sorder_desc, type(sorder_desc)))
            return []

        l = sorder_desc.split(':')
        return [ self._ORDER_MAP[i] for i in l if i in self._ORDER_MAP ]

    def search(self, page, n_per_page, category_name, keyword, city, location=None, ords=None, version=1):
        """LOGIC:
        支持两类搜索："类目搜索"和"关键字搜索"
        其中，类目搜索支持 (前台类目和后台类目，具体由version控制)
        @类目搜索:
        version 1 => for backend category
        version 2 => for foreground category

        @:关键字搜索 (目前与类目没有关系)
        if keyword: -> se_client.search(...)
        """
        p = FilterParameterBarebone()

        # only for version 1, backend category as search field
        if category_name and version == 1:
            p &= FieldFilterParameter(name='category', value=category_name)
        if city:
            p &= FieldFilterParameter(name='city', value=city)

        # # only leak out those Audited.
        # p &= FieldFilterParameter(name='status', value='Audited')

        must = []
        if keyword:
            must.append( QueryStringQueryParameter( fields='title', query_string=keyword) )

        # TODO: Formula acts weired.
        fml = Formula(p, query_must=must,  query_must_not=[], query_should=[], sort_orders=[])

        sort_ords = self._sorder_desc2macro(ords)
        for sord in sort_ords:
            so = None
            if sord == 'LOCATION':
                if not location:
                    self._logging.warn("no location found which is asked to be as sort factor")
                else:
                    so = SEGeoDistanceSortOrder(field='location', order=SE_ORDER_ASC, lat=location.lat, lon=location.lon)
            elif sord == 'CREATE_TIME':
                so = SESortOrder('create_time', SE_ORDER_DESC)
            elif sord == 'UPDATE_TIME':
                so = SESortOrder('update_time', SE_ORDER_DESC)
            elif sord == 'END_TIME':
                so = SESortOrder('end_time', SE_ORDER_DESC)
            else:
                self._logging.warn("undefined sort order:'%s', ignore it" % sord)

            # store it if necessary
            if so:
                fml.addSortOrder(so)

        # always make sure location is one of sort order factor
        if 'LOCATION' not in sort_ords:
            so_geo = SEGeoDistanceSortOrder(field='location', order=SE_ORDER_ASC, lat=location.lat, lon=location.lon)
            fml.addSortOrder(so_geo)

        try:
            # if version is 1(that is, backend category search) or 'keyword search' => search
            if version == 1 or keyword:
                self._logging.info("using search ...")
                return seclient.search( fml.represent(), page_index=page, count_per_page=n_per_page )
            # frontend category search
            if version == 2:
                self._logging.info("using getCategoryContentsByName ...")
                return seclient.getCategoryContentsByName(category_name,
                                                          page_index=page,
                                                          count_per_page=n_per_page,
                                                          formula=fml.represent() )
            # backup
            self._logging.info("using search as backup ...")
            return seclient.search( fml.represent(), page_index=page, count_per_page=n_per_page )
        except Exception as e:
            self._logging.error("error occurs while searching, caz:'%s'" % e)
            return None

    def getCategories(self):
        try:
            leak_attr = ['name', 'cn_name', 'icon_view', 'icon_pressed','description']
            cats = seclient.getCategories()
            cats = [ { k:v for k,v in i.items() if k in leak_attr } for i in cats ]
            for i in cats:
                i['children'] = []
            return cats
        except Exception as e:
            self._logging.error("error occurs while getCategories, caz:'%s'" % e)
            return None
