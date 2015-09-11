#!/usr/bin/enb python
#coding:utf8

"""
all global transform funcs
"""

import json
import re
from usopp_ctrl import usopp_client
from encrypta_ctrl import EncryptaCtrl
from leobase.leo_event_time import LeoEventTime
from sputnik.SpuLogging import SpuLogging
from sputnik.SpuDebug import SpuDebugBlock
from leobase.leo_count import leo_collect_count, leo_detail_count
from leobase.base_ctrl import gen_price_info

_LOGGING = SpuLogging(module_name='transform', class_name='LeoTransform')

def get_property_value(property_obj, default_value):
    if not property_obj:
        return None
    return property_obj.get('property_value', default_value)

class LeoTransform(object):
    
    CATE_HOTEL = 1
    CATE_SIGHT = 2

    def __init__(self):
        pass

    def _get_poi_by_ps_2(self, leo):
        """免费&不需要报名"""

        # from leo or sku
        leo_target_type = leo.leo.fields['target_type']
        if leo_target_type == 'barebone':
            props_target = leo.leo
        elif leo_target_type == 'sku':
            props_target = leo.sku

        poi = get_property_value(
            props_target.property_values.get('poi', None), None)

        # None or ''
        if not poi:
            poi = get_property_value(
                props_target.property_values.get('server_biz_name', None), '')
        return poi

    def _get_poi_by_ps_103(self, leo):
        """付费&能从leo系统购买，官方发布的活动"""

        # only from sku
        poi = get_property_value(
            leo.sku.property_values.get('poi', None), None)
        
        # not None or ''
        if not poi:
            poi = get_property_value(
                leo.sku.property_values.get('server_biz_name', None), '')
        return poi

    def _get_poi_by_ps_101(self, leo):
        """付费&能从leo系统购买, 第三方平台资源"""

        # from leo or sku or hotel resources
        # find order leo > sku > resources
        for target in [leo.leo, leo.sku]:
            poi = get_property_value(
                target.property_values.get('poi', None), None)
            # not None or ''
            if poi:
                return poi

        # hotel resources
        for resource in leo.resources:
            if resource.category.id == self.CATE_HOTEL:
                return resource.sku.fields.get('cn_name', '')
        return ''

    def get_poi(self, leo):
        """
        switch condtion is participate_status
        detail look http://redmine.meishixing.com/projects/mibang-project-
        activities-backend-leo/wiki/Leo_participate_value_%E8%AF%A6%E6%83%85
        """

        ps = int(leo.leo.fields['participate_status'])
        fn = '_get_poi_by_ps_%s' % ps
        if not hasattr(self, fn):
            _LOGGING.error('get_poi failed unknow participate_status leo:%s ps:%s',
                           leo.leo.fields['id'], ps)
            return ''
        return getattr(self, fn)(leo)

    get_hotel_name = get_poi

    def get_poi_v2(self, leo):
        """
        switch condtion is participate_status
        detail look http://redmine.meishixing.com/projects/mibang-project-
        activities-backend-leo/wiki/Leo_participate_value_%E8%AF%A6%E6%83%85
        """
        poi = leo.poi or leo.server_biz_name or ''
        ps = int(leo.participate_status)
        if poi is '' and ps == 101 and int(leo.category_id) == 3:
            for resource in leo.resources:
                if int(resource.category_id) == self.CATE_HOTEL:
                    return resource.cn_name
        return poi

    def _get_address_by_ps_2(self, leo):
        """免费&不需要报名"""

        # from leo or sku
        leo_target_type = leo.leo.fields['target_type']
        if leo_target_type == 'barebone':
            props_target = leo.leo
        elif leo_target_type == 'sku':
            props_target = leo.sku

        address = get_property_value(
            props_target.property_values.get('address', None), None)

        return address

    def _get_address_by_ps_103(self, leo):
        """付费&能从leo系统购买，官方发布的活动"""

        # only from sku
        address = get_property_value(
            leo.sku.property_values.get('address', None), None)
        
        return address

    def _get_address_by_ps_101(self, leo):
        """付费&能从leo系统购买, 第三方平台资源"""

        # from hotel resources
        for resource in leo.resources:
            if resource.category.id == self.CATE_HOTEL:
                address = get_property_value(
                    resource.sku.property_values.get('address', None), None)
                if address:
                    return address
                return ''
        return ''

    def get_address(self, leo):
        """
        switch condtion is participate_status
        detail look http://redmine.meishixing.com/projects/mibang-project-
        activities-backend-leo/wiki/Leo_participate_value_%E8%AF%A6%E6%83%85
        """

        ps = int(leo.leo.fields['participate_status'])
        fn = '_get_address_by_ps_%s' % ps
        if not hasattr(self, fn):
            _LOGGING.error('get_address failed unknow participate_status leo:%s ps:%s',
                           leo.leo.fields['id'], ps)
            return ''
        return getattr(self, fn)(leo)

    def get_address_v2(self, leo):
        """
        switch condtion is participate_status
        detail look http://redmine.meishixing.com/projects/mibang-project-
        activities-backend-leo/wiki/Leo_participate_value_%E8%AF%A6%E6%83%85
        """
        address = leo.address or ''
        ps = int(leo.participate_status)
        if address == '' and ps == 101:
            for resource in leo.resources:
                if int(resource.category_id) == self.CATE_HOTEL:
                    return resource.address
        return address
    
    def get_tags(self, leo):
        return [t.name for t in leo.tags]

    def get_category(self, leo):
        return leo.category.cn_name

    def get_category_id(self, leo):
        return leo.category.id

    def _get_price_by_ps_2(self, leo):
        """免费&不需要报名"""
        leo_target_type = leo.leo.fields['target_type']
        if leo_target_type == 'barebone':
            props_target = leo.leo
        elif leo_target_type == 'sku':
            props_target = leo.sku

        price_val = get_property_value(
            props_target.property_values.get('price_info', None), None)
        if price_val:
            re_result = re.search(r'(\d+(:?\.\d+)?)', str(price_val))
            if re_result:
                return re_result.groups()[0]
            return 0.0
        return 0.0

    def _get_price_by_ps_101(self, leo):
        """付费&能从leo系统购买, 第三方平台资源"""

        # from sku or goods
        # find order sku min_price > goods min_price >
        #            sku quoted_price > sku advice_min_price
        
        for (target, prop) in [(leo.sku, 'min_price'),
                               (leo.goods, 'min_price'),
                               (leo.sku, 'quoted_price'),
                               (leo.sku, 'advice_min_price')]:
            price_val = get_property_value(
                target.property_values.get(prop, None), None)
            if price_val:
                return price_val
        return 0.0

    def _get_price_by_ps_103(self, leo):
        """付费&能从leo系统购买，官方发布的活动"""
        # from sku or leo
        # find order sku min_price > leo min_price
        
        for (target, prop) in [(leo.sku, 'min_price'),
                               (leo.leo, 'min_price')]:
            price_val = get_property_value(
                target.property_values.get(prop, None), None)
            if price_val:
                return price_val
        return 0.0

    def get_price(self, leo):
        """
        return (sell_price, price)
        like get_poi
        """
        ps = int(leo.leo.fields['participate_status'])
        fn = '_get_price_by_ps_%s' % ps
        if not hasattr(self, fn):
            _LOGGING.error('get_price failed unknow participate_status leo:%s ps:%s',
                           leo.leo.fields['id'], ps)
            return (0.0, 0.0)

        price = 0.0
        def except_func(exc_value):
            _LOGGING.error('fn failed leo:%s m:%s', leo.leo.fields['id'], exc_value)
        
        with SpuDebugBlock(except_func):
            price = getattr(self, fn)(leo)
            price = round(float(price), 2)

        return (price, price)

    def get_price_v2(self, leo):
        """
        return (sell_price, price)
        like get_poi
        """
        ps = int(leo.participate_status)
        price = 0.0
        price_info = leo.price_info or ''
        if ps == 2:
            price = leo.price_info or 0.0
            if price:
                # fixbug: 100-200
                re_result = re.search(r'(\d+(:?\.\d+)?)', str(price))
                if re_result:
                    price = re_result.groups()[0]
                else:
                    price = 0.0
        elif ps == 101:
            price = leo.min_price or leo.quoted_price or leo.advice_min_price or 0.0
        elif ps == 103:
            if int(leo.min_price) != -1:
                price = leo.min_price
            else:
                price_list = [sku.min_price for sku in leo.resources]
                if price_list:
                    price = min(price_list)
                else:
                    price = 0

            if not leo.price_info or len(leo.price_info) < 1:
                price_dict = gen_price_info(leo.resources)
                price_info = price_dict.get('price_info', '')

        else:
            _LOGGING.error('get_price failed unknow participate_status leo_id:%s ps:%s',
                           leo.id, ps)
            return (0.0, 0.0)

        price = price if type(price) is float else float(price)
        price = round(price, 2)

        return (price, price_info)

    def get_biz_phone(self, leo):
        ps = int(leo.leo.fields['participate_status'])
        if ps not in (103,):
            return ''
        biz_phone = get_property_value(
            leo.sku.property_values.get('biz_phone', None), None)
        if biz_phone:
            return biz_phone
        return ''

    def get_biz_phone_v2(self, leo):
        return leo.biz_phone

    def get_consult_phone(self, leo):
        return leo.consult_phone or leo.biz_phone or ''

    def get_hotel_address(self, leo):
        ''' deprecated '''
        if not leo.resources:
            address = leo.sku.property_values.get('address', None)
            if not address:
                return ''
            return address.get('property_value', '')

        for resource in leo.resources:
            if resource.category.id == self.CATE_HOTEL:
                address = resource.sku.property_values.get('address', None)
                address = address.get('property_value', None)
                if address:
                    return address
        return ''
    
    def _get_specific_address(self, info):
        # zhima
        address = info.get('address', None)
        if not address:
            return ''
        return address.get('property_value', '')

    def get_title(self, leo):
        return leo.leo.fields['cn_name']

    def get_title_v2(self, leo):
        return leo.cn_name

    def get_leo_id(self, leo):
        return leo.leo.fields['id']


    def get_time_info(self, leo):
        time_letd = leo.sku.property_values.get('time_letd', None)
        if time_letd is None:
            return ''
        time_letd_src = time_letd.get('property_value', '')
        if time_letd_src is '':
            return ''

        try:
            time_letd = eval(time_letd_src)
        except Exception as m:
            _LOGGING.error('get_time_info failed evel time_letd:%s time_letd_src:%s ' \
                           'exception:%s', time_letd, time_letd_src, m)
            return ''

        if 'option' in time_letd and \
           'more_desc' in time_letd and \
           'type' in time_letd:
            return self.get_time_info_by_letd(time_letd_src, leo)
        return self.get_time_info_by_lms_format(time_letd, leo)

    def get_time_info_v2(self, leo):
        time_letd_src = leo.time_letd
        if time_letd_src is '':
            return ''

        try:
            time_letd = eval(time_letd_src)
        except Exception as m:
            _LOGGING.error('get_time_info failed evel time_letd:%s time_letd_src:%s ' \
                           'exception:%s', time_letd, time_letd_src, m)
            return ''

        if 'option' in time_letd and \
           'more_desc' in time_letd and \
           'type' in time_letd:
            return self.get_time_info_by_letd(time_letd_src, leo)
        return self.get_time_info_by_lms_format(time_letd, leo)

    def get_time_info_by_letd(self, time_letd, leo):
        leo_event_time = LeoEventTime()
        try:
            leo_event_time.loads(time_letd)
            desc = leo_event_time.get_realtime_desc()
        except Exception as m:
            _LOGGING.error('get_time_info_by_letd failed leo:%s time_letd:%s exception:%s',
                           leo, time_letd, m)
            return ''
        return desc

    def get_time_info_by_lms_format(self, option, leo):
        leo_event_time = LeoEventTime()        
        time_style = option.get('time_style', 'rangeDay')
        
        def make_oneday(ts):
            leo_event_time.make_oneday(ts['day'],
                                       ts['start_time'],
                                       ts['end_time'])

        def make_time_range(ts):
            if 'start_day' in ts:
                start_time = '%(start_day)s %(start_time)s' % ts
                end_time = '%(end_day)s %(end_time)s' % ts
            else:
                start_time = ts['start_time']
                end_time = ts['end_time']
            leo_event_time.make_time_range(start_time,
                                           end_time)

        def make_continue_day(ts):
            leo_event_time.make_continue_day(ts['start_day'], ts['end_day'],
                                             ts['start_time'], ts['end_time'])

        def make_week(ts):
            leo_event_time.make_week(ts['event_weekdays'], ts['days'], ts['times'])

        def make_intermittent(ts):
            leo_event_time.make_intermittent(ts['time_list'])

        time_style_func = {
            'oneDay': lambda s: make_oneday(s),
            'continueDay': lambda s: make_continue_day(s),
            'rangeDay': lambda s: make_time_range(s),
            'weekDay': lambda s: make_week(s),
            'interDay': lambda s: make_intermittent(s)
        }

        try:
            time_style_func[time_style](option)
        except Exception as m:
            _LOGGING.error('get_time_info failed time_style_func option:%s ' \
                           'leo:%s exception:%s',
                           option, leo, m)
            return ''

        return leo_event_time.get_realtime_desc()

    def get_time_desc(self, leo):
        ps = int(leo.leo.fields['participate_status'])
        if ps not in (2, 103):
            return ''
        if ps is 103:
            time_desc = get_property_value(
                leo.sku.property_values.get('time_desc', None), None)
        else:
            leo_target_type = leo.leo.fields['target_type']
            if leo_target_type == 'barebone':
                props_target = leo.leo
            elif leo_target_type == 'sku':
                props_target = leo.sku
            time_desc = get_property_value(
                props_target.property_values.get('time_desc', None), None)

        return '' if time_desc is None else time_desc

    def get_time_desc_v2(self, leo):
        return leo.time_desc or ''

    def encrypt_to_number(self, data):
        encrypta = EncryptaCtrl()
        encrypta_data = encrypta.encrypt(data, version=3)
        if encrypta_data['ok']:
            _LOGGING.debug('encrypt_to_number data_src:%s encrypt_data:%s',
                           data, encrypta_data)
            return int(encrypta_data['data'])
        _LOGGING.error('encrypt_to_number failed data:%s msg:%s',
                       data, encrypta_data['why'])
        return None

    def get_leo_list(self, leo_ins_list):
        leo_list = []
        for leo_ins in leo_ins_list:
            leo = {}
            leo['leo_id'] = self.get_leo_id(leo_ins)
            leo['category'] = self.get_category(leo_ins)
            leo['category_id'] = self.get_category_id(leo_ins)
            leo['price'] = self.get_price(leo_ins)[0]
            leo['poi_name'] = self.get_hotel_name(leo_ins)
            leo['poi_address'] = self.get_hotel_address(leo_ins)
            leo['front_cover_image'] = leo_ins.images[:5]
            leo['title'] = self.get_title(leo_ins)
            leo['tags'] = self.get_tags(leo_ins)
            leo['show_free'] = False
            leo['time_info'] = self.get_time_info(leo_ins)
            leo_list.append(leo)
        return leo_list
    
    def trans_leo(self, leo_ins):
        leo = {}
        leo['leo_id'] = self.get_leo_id(leo_ins)
        leo['category'] = self.get_category(leo_ins)
        leo['price'] = self.get_price(leo_ins)[0]
        leo['poi_name'] = self.get_hotel_name(leo_ins)
        leo['poi_address'] = self.get_hotel_address(leo_ins)
        leo['front_cover_image'] = leo_ins.images[:5]
        leo['title'] = self.get_title(leo_ins)
        leo['tags'] = self.get_tags(leo_ins)
        leo['show_free'] = False
        leo['time_info'] = self.get_time_info(leo_ins)
        return leo

    def get_weekend_event(self, lat, lon):
        _LOGGING.debug('get_weekend_event lat:%s lon:%s', lat, lon)
        weekend_events = []
        try:
            event_list = usopp_client.getActivitys(True, True, False, 1, 1000,
                                                   -1, lat=lat, lon=lon)
            weekend_events = json.loads(event_list.rst)["activitys"]
        except Exception as m:
            _LOGGING.error('get_weekend_event failed lat:%s lon:%s type:%s msg:%s',
                           lat, lon, type(m), m)
        _LOGGING.info('get_weekend_event: %s', weekend_events)
        return weekend_events

    def get_collect_count(self, leo_id):
        return leo_collect_count.get_count(leo_id)

    def get_view_count(self, leo_id):
        return leo_detail_count.get_count(leo_id)

    def get_collect_counts(self, leo_ids):
        return leo_collect_count.get_multi_counts(leo_ids)

    def get_view_counts(self, leo_ids):
        return leo_detail_count.get_multi_counts(leo_ids)
