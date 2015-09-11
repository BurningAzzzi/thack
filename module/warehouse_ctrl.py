#! /usr/bin/env python
# -*- coding: utf-8 -*-

import json

from sputnik.SpuLogging import SpuLogging
from sputnik.SpuPythonObject import SDict, SList, STuple

from base_ctrl import WAREHOUSE_RPC_ADDRESS, RTC_CNF
from pandabase.rpcservice import *
from seraph_ctrl import *
from warehouse.ttypes import *
from warehouse_client import WarehouseClient, g_wh_db_info
from encrypta_ctrl import EncryptaCtrl
import re
from mapicon_ctrl import MapIconCtrl
from leobase.base_ctrl import unicode_to_md5, gen_price_info
from leobase.pa.pa import ProductAssembly

OPS_INFO = {'operator':'leo', 'channel': 'leo', 'channel_info': 'leo'}

SpuLogging.info("\tRPC warehouse address:%s,\t port:%s" % (WAREHOUSE_RPC_ADDRESS[0], WAREHOUSE_RPC_ADDRESS[1]))
warehouse_client = WarehouseClient()
warehouse_client.connect(WAREHOUSE_RPC_ADDRESS[0], WAREHOUSE_RPC_ADDRESS[1])
warehouse_client.setOpsInfo(OPS_INFO)

resource = {'warehouse_client': warehouse_client}
ProductAssembly.global_initialize(RTC_CNF, resource)


def toString(var):
    default_return_string = ''
    if isinstance(var, str):
        return var
    if isinstance(var, unicode):
        try:
            return var.encode('utf-8')
        except Exception as e:
            return default_return_string
    # others
    try:
        return str(var)
    except Exception as e:
        return default_return_string


class WarehouseCtrl(object):
    # TODO these two macro should be set by warehouse, and can edited by 'leo_admit'
    _DEFALUT_MAX_NUM_PER_ONESHOT = 99
    _DEFALUT_MIN_NUM_PER_ONESHOT = 1

    _DEFAULT_PAY_MODE = 1

    _logging = SpuLogging(module_name='warehouse_ctrl', class_name='WarehouseCtrl')
    _category_specified_props_map = {
        'hotel': [
            'room_size',
            'bed_size',
            'extra_bed_available',
            'extra_bed_price',
            'wifi',
            'bed_type',
            'shower_equipment',
            ],
        'sight': [
            'ticket_max_book_count',
            'ticket_description',
            'book_address',
            'credential',
            'order_tips',
            ],
        'scenic': []
        }
    _def_val_type = 'string'
    _def_return_vals = {
        'object': {},
        'array': [],
        'string': '',
        'bool':False,
        'int':-1,
        'float':-1.00,
        }

    def __init__(self, ):
        self.why = ''
        self.mapicon = MapIconCtrl()
        self.encryta = EncryptaCtrl()
        self.exclusive_tag_ids = [1,2,3,4]

    def reset_why(self,):
        self.why = ''

    def _convert_value_with_type(self, val, prop_val_type):
        def _inner_f_text(val): return val
        def _inner_f_string(val): return val
        def _inner_f_int(val): return int(val)
        def _inner_f_float(val): return float(val)
        def _inner_f_bool(val): return val in [True, 'true', 'True', '1', 1]
        def _inner_f_array(val): return str(val)
        def _inner_f_object(val): return str(val)
        _value_ops_map = {
            'text'   : _inner_f_text,
            'string' : _inner_f_string,
            'int'    : _inner_f_int,
            'float'  : _inner_f_float,
            'bool'   : _inner_f_bool,
            'array'  : _inner_f_array,
            'object' : _inner_f_object
            }
        if prop_val_type not in _value_ops_map.keys():
            return self._def_return_vals[prop_val_type]
        try:
            f = _value_ops_map[prop_val_type]
            ret = f(val)
            self._logging.debug("type:'%s', raw:'%s', after:'%s'" % (prop_val_type, val, ret))
            return ret
        except Exception as e:
            self._logging.error("[CHCK] exception caught type:'%s', raw:'%s', exc:'%s'" % (prop_val_type, val, e))
            return self._def_return_vals[prop_val_type]

    def _gen_template_id(self, leo):
        if leo._category.id == 3: return 2  # 周边游
        if leo._category.id == 17: return 3 # 景点
        # default
        return 1                # 活动

    def _conv(self, value, f=None, default=None):
        if f:
            try:
                return f(value)
            except Exception as e:
                self._logging.error("exc: '%s'" % e)
                return default
        else:
            return value

    def _gattr(self, leo, attr_name, default=None, f=None):
        try:
            x = getattr(leo, attr_name) or default
            return f(x) if f else x
        except Exception as e:
            self._logging.error("exc: '%s'" % e)
            return default

    def getLeoDetails(self, leo_id, session_id, extra_params):
        """refer to resource/leo_detail.json for details
        """
        self.reset_why()
        # start
        try:
            leo = warehouse_client.getLeoV2( leo_id )
        except Exception as e:
            self._logging.error("exception caught while get leo:'%s', exc:'%s'" % (leo_id, e))
            return None
        # compose specificed handler
        leo_detail_handler_name = '_leo_detail_' + str(leo.participate_status)
        if not hasattr(self, leo_detail_handler_name):
            self.why = "leo:'%s', no handler named:'%s'" % (leo_id, leo_detail_handler_name )
            self._logging.error( self.why )
            return None
        # ok, handle it
        leo_detail_handler = getattr(self, leo_detail_handler_name)
        self._logging.info("leo:'%s', trying to handle leo by handler:'%s'" % (leo_id, leo_detail_handler_name))
        # finally, set participate_status and return
        leo_detail = leo_detail_handler( leo, extra_params )
        if leo_detail:
            leo_detail['collected'] = self._is_leo_been_collected_by_user(leo.id, session_id)
            leo_detail['participate_status'] = int(leo.participate_status)

        # use ProductAssembly append leo
        pa = ProductAssembly(None)
        pa.detail(leo, sight_result=leo_detail)

        # append comm info
        self._leo_detail_comm_info(leo, leo_detail)

        return leo_detail

    def _process_time(self, target):
        start_time = target.start_time or ''
        end_time = target.end_time or ''
        info = target.time_desc

        def _is_in_standard_time_format(raw_time):
            """if true: return (date_part, time_part), else, None is returned
            standard_time_format: '2014/01/01 00:00:00' or '2014-01-01 00:00:00'
            """
            valid_time_pattern = '(\d{4})([/-])(\d{2}[/-]\d{2}) +(\d{2}:\d{2}):(\d{2})'
            res = re.match(valid_time_pattern , raw_time)
            return res.groups() if res else None
        def is_hms_default_value(var_s_hms, var_e_hms):
            def_start_hms, def_end_hms = '00:00:00', '23:59:59'
            # NOTICE: make sure following default values are consistent with lms system
            return (var_s_hms == def_start_hms or var_e_hms == def_end_hms)

        # refine 'info' if necessary
        self._logging.info("default info:'%s'" % info)
        if not info:
            self._logging.info("tring to refine 'info' by leo itself with s:'%s', e:'%s'" % (start_time, end_time))
            s,e = _is_in_standard_time_format(start_time), _is_in_standard_time_format(end_time)
            if s is None or e is None:
                return dict(start='', end='', info='')
            # now, both are in standard time format
            s_year, s_yd_sep, s_date, s_hm, e_sec, s_hms = s[0],s[1],s[2],s[3],s[4],s[3]+':'+s[4]
            e_year, e_yd_sep, e_date, e_hm, e_sec, e_hms = e[0],e[1],e[2],e[3],e[4],e[3]+':'+e[4]
            # only use date if 'year' is same, else, 'year' should be pre-added.
            is_same_year = (s_year == e_year)
            is_same_day = (s_year == e_year) and (s_date == e_date)
            # handle year and date part
            if is_same_day:
                info = "%s%s%s" % (s_year, s_yd_sep, s_date) # use s_yd_sep other than e_yd_sep
            elif is_same_year:
                info = "%s%s%s~%s" % (s_year, s_yd_sep, s_date, e_date)
            else:
                info = "%s%s%s~%s%s%s" % (s_year, s_yd_sep, s_date, e_year, e_yd_sep, e_date)
            # handle hms separately
            if not is_hms_default_value(s_hms, e_hms):
                info += " %s~%s" % (s_hm, e_hm)

        return dict(start=start_time, end=end_time, info=info)

    def _compose_lrzm_tips(self, leo, v=0):
        lrzm_tips = self._conv(leo.lrzm_tips or '[]', f=json.loads)
        if v >=4:
            # handle booking_XXX
            booking_tip_content = []
            if leo.booking_day:
                tip = {'t':'text', 'v':'请提前%s天预约。' % leo.booking_day}
                booking_tip_content.append(tip)
            if leo.booking_phone:
                tip = [ {'t':'text', 'v':"预约电话："} ,
                  {'t':'phone', 'v':str(leo.booking_phone)} ,
                  {'t':'text', 'v':"。"} ]
                booking_tip_content.extend(tip)
            if booking_tip_content:
                booking_tip = {'type':'list', 'content': booking_tip_content }
                lrzm_tips.append(booking_tip)

        else:                   # for old versions
            # booking_XXX
            booking_tip_content = []
            vtip = ''
            if leo.booking_day:
                vtip = '请提前%s天预约。' % leo.booking_day
            if leo.booking_phone:
                vtip += '预约电话：%s。' % leo.booking_phone
            if vtip:
                lrzm_tips.append( {'type':'text', 'content':vtip} )

        return lrzm_tips

    def _compose_desc(self, leo, v, raw_desc, lrzm_tips):
        """@raw_desc: [{...}, {...}]
        @lrzm_tips: [{...}, {...}]
        """
        if v >= 2:
            desc = raw_desc
        else:                   # for old versions
            lrzm_tips_content = [toString('|懒人提示|')] + ['%s %s' % (toString('·'), toString(i['content'])) for i in lrzm_tips if i['type'] == 'text']
            lrzm_tips = [ { 'type':'text', 'content': '\n'.join( lrzm_tips_content ) } ]
            desc = raw_desc + lrzm_tips
            self._logging.info("merging description with lrzm_tips, for version:'%s'..." % v)

            # booking_XXX
            booking_tip_content = []
            vtip = ''
            if leo.booking_day:
                vtip = '请提前%s天预约。' % leo.booking_day
            if leo.booking_phone:
                vtip += '预约电话：%s。' % leo.booking_phone
            if vtip:
                desc.append( {'type':'text', 'content':vtip} )

        return desc

    def _get_desc(self, leo_id):
        try:
            desc = warehouse_client.getDescription(target_type='leo', target_id=long(leo_id))
            return json.loads(desc)
        except TIOError as e:
            self._logging.warn("leo:'%s', [CHCK] exception caught while converting 'description', why:'%s'" % (leo_id, e))
            return []
        except Exception as e:
            self._logging.warn("leo:'%s', [CHCK] exception caught while converting 'description', why:'%s'" % (leo_id, e))
            return []

    def _origin_price(self, leo_origin_price):
        """return string"""
        if leo_origin_price in [None, -1.0, -1, 0]:
            return ''
        return str(leo_origin_price)

    def _provider(self, server_biz_name, leo_source_id):
        """
        provider logic:
        1. leo.server_biz_name
        2. seraph.biz_name
        """
        if server_biz_name:
            return server_biz_name
        try:
            biz = get_biz(long(leo_source_id))
            return biz.biz_name
        except Exception as e:
            self._logging.error("failed to get biz name from seraph, biz_id:'%s'" % leo_source_id)
            return ''
        #finally
        return ''

    def _leo_detail_2(self, leo, extra_params):
        """ refer wiki on participate_status's value is 2
        """
        ret = {}
        ret['template_id'] = self._gen_template_id(leo)
        ret['mapicon'] = self.mapicon.get_mapicon(leo._category.id)
        ret['category'] = dict(cn_name=leo._category.cn_name, id=leo._category.id, icon_view=self.mapicon.getDetailCategoryIcon(leo._category.id))
        ret['title'] = leo.cn_name
        ret['leo_target_type'] = leo.target_type
        ret['leo_target_id'] = int(leo.target_id) or -1
        ret['time'] = self._process_time(leo)
        ret['location'] = dict(lat=leo.lat, lon=leo.lon)
        ret['address'] = leo.address or ''
        ret['price_info'] = leo.price_info or ''
        ret['main_title'] = leo.main_title or ''
        ret['sub_title'] = leo.sub_title or ''
        ret['server_biz_name'] = leo.server_biz_name or ''
        ret['poi'] = leo.poi or leo.server_biz_name or ''
        ret['images'] = leo.images
        ret['tags'] = [ dict(name=i.name, id=i.id) for i in leo.tags if i.id not in self.exclusive_tag_ids ] if leo.tags else []
        ret['providers'] = ret['provider'] = self._provider(leo.server_biz_name, leo.source_id)
        ret['consult_phone'] = leo.consult_phone or leo.biz_phone or ''
        ret['lrzm_tips'] = self._compose_lrzm_tips(leo, extra_params['v'])
        ret['description'] = self._compose_desc(leo, extra_params['v'], self._get_desc(leo.id), ret['lrzm_tips'])
        ret['booking_policy'] = self._conv(leo.booking_policy or '[]', f=json.loads)
        ret['ticket_usage'] = self._conv(leo.ticket_usage or '[]', f=json.loads)
        ret['ticket_rule'] = self._conv(leo.ticket_rule or '[]', f=json.loads)
        ret['biz_phone'] = leo.biz_phone or leo.consult_phone or ''
        ret['consult_phone'] = leo.consult_phone or leo.biz_phone or ''
        ret['biz_website'] = leo.biz_website or ''
        # delete, use sku pay_type
        #ret['pay_mode'] = leo.pay_mode or self._DEFAULT_PAY_MODE
        ret['pay_method_list'] = self._get_pay_methods(leo.biz_id)
        return ret

    def _get_pay_methods(self, biz_id):
        try:
            biz_info = seraph_client.getBiz(int(biz_id))
            return biz_info.pay_method_list
        except TIOError as e:
            self._logging.warn("[CHECK] no pay methods gotten from seraph by biz_id:'%s', exc:'%s'" % (biz_id, e))
        except Exception as e:
            self._logging.warn("[CHECK] no pay methods gotten from seraph by biz_id:'%s', exc:'%s'" % (biz_id, e))
        # always return [].
        return []

    def get_leo_by_biz_id(self, biz_id, session_id, page=1, page_size=20):
        try:
            leo_info_list = warehouse_client.getLeosByBizId(int(biz_id), page_index=page, n_per_page=page_size)
            return [{"leo_id": int(leo.id)} for leo in leo_info_list]
        except Exception as e:
            self._logging.error("exc: '%s'" % str(e))
            return []
        # result = []
        # for leo in leo_info_list:
        #     leo_detail_handler_name = '_leo_detail_' + str(leo.participate_status)
        #     if not hasattr(self, leo_detail_handler_name):
        #         self.why = "leo:'%s', no handler named:'%s'" % (leo_id, leo_detail_handler_name )
        #         self._logging.error( self.why )
        #         return None
        #     # ok, handle it
        #     leo_detail_handler = getattr(self, leo_detail_handler_name)
        #     self._logging.info("leo:'%s', trying to handle leo by handler:'%s'" % (leo.id, leo_detail_handler_name))
        #     # finally, set participate_status and return
        #     leo_detail = leo_detail_handler(leo, extra_params=extra_params)
        #     if leo_detail:
        #         leo_detail['collected'] = self._is_leo_been_collected_by_user(leo.id, session_id)
        #         leo_detail['participate_status'] = int(leo.participate_status)

        #         # use ProductAssembly append leo
        #         pa = ProductAssembly(None)
        #         pa.detail(leo, sight_result=leo_detail)

        #         # update leo total sell status
        #         self._leo_total_sell_restriction(leo, leo_detail)
        #         result.append(leo_detail)
        # return result

    def _multi_sku_min_price(self, leo):
        if int(leo.min_price) != -1:
            return leo.min_price
        price_list = [sku.min_price for sku in leo.resources]
        if price_list:
            return min(price_list)
        else:
            return 0

    def _multi_sku_price_info(self, leo):
        if leo.price_info and len(leo.price_info) > 0:
            return leo.price_info
        resources = [vars(resource) for resource in leo.resources]
        price_dict = gen_price_info(leo.resources)
        return price_dict.get('price_info', '')

    def _leo_detail_103(self, leo, extra_params):
        """http://redmine.meishixing.com/projects/mibang-project-activities-backend-leo/wiki/Leo_participate_value_%E8%AF%A6%E6%83%85
        """
        def _inner_refine_booking_policy(leo):
            """
            participate_status == 103: -> not third-party api providers.
            source_id == 1000: -> mibang
            """
            booking_policy = self._conv(leo.booking_policy or '[]', f=json.loads)
            if int(leo.source_id) != 1000:
                item = { 'type':'text', 'content': toString("为了保证您的权益，请选择懒人周末线上支付，如使用其他方式交易并在消费中产生的纠纷，懒人周末无法帮您进行调节并不承担责任，感谢您的理解与支持。")}
                booking_policy.append( item )
            return booking_policy


        ret = {}
        ret['template_id'] = self._gen_template_id(leo)
        ret['mapicon'] = self.mapicon.get_mapicon(leo._category.id)
        ret['category'] = dict(cn_name=leo._category.cn_name, id=leo._category.id, icon_view=self.mapicon.getDetailCategoryIcon(leo._category.id))
        ret['title'] = leo.cn_name
        ret['leo_target_type'] = leo.target_type
        ret['leo_target_id'] = int(leo.target_id)

        #ret['pay_mode'] = leo.pay_mode or self._DEFAULT_PAY_MODE
        ret['pay_method_list'] = self._get_pay_methods(leo.biz_id)
        ret['time'] = self._process_time(leo)
        ret['location'] = dict(lat=leo.lat, lon=leo.lon)
        ret['city'] = leo.city or ''
        ret['address'] = leo.address or ''
        ret['poi'] = leo.poi or leo.server_biz_name or ''

        ret['price_info'] = self._multi_sku_price_info(leo)
        ret['min_price'] = self._multi_sku_min_price(leo)
        ret['origin_price'] = self._origin_price(leo.quoted_price)

        ret['main_title'] = leo.main_title or ''
        ret['sub_title'] = leo.sub_title or ''
        ret['server_biz_name'] = leo.server_biz_name or ''

        ret['biz_phone'] = leo.biz_phone or leo.consult_phone or ''
        ret['biz_website'] = leo.biz_website or ''
        ret['sell_restriction'] = self._process_sell_restriction(leo)
        ret['images'] = leo.images
        ret['tags'] = [ dict(name=i.name, id=i.id) for i in leo.tags if i.id not in self.exclusive_tag_ids ] if leo.tags else []
        ret['is_can_book'] = True

        ret['sku_representation'] = self._compose_sku_representation(leo)
        ret['trans_params'] = self._compose_trans_params(leo)

        ret['providers'] = ret['provider'] = self._provider(leo.server_biz_name, leo.source_id)
        ret['consult_phone'] = leo.consult_phone or leo.biz_phone or ''
        ret['lrzm_tips'] = self._compose_lrzm_tips(leo, extra_params['v'])
        ret['description'] = self._compose_desc(leo, extra_params['v'], self._get_desc(leo.id), ret['lrzm_tips'])
        ret['booking_policy'] = _inner_refine_booking_policy(leo)
        ret['ticket_usage'] = self._conv(leo.ticket_usage or '[]', f=json.loads)
        ret['ticket_rule'] = self._conv(leo.ticket_rule or '[]', f=json.loads)

        return ret

    def _is_leo_been_collected_by_user(self, leo_id, session_id):
        # get info from pandaservice
        try:
            leo_id = long(leo_id)
            is_login, user_id = check_login(str(session_id))
            self._logging.info("is_login:'%s', user_id:'%s', session_id:'%s'"% (is_login, user_id, session_id))
            # if not is_login: return False
        except Exception as e:
            self._logging.warn("exception caught while check login, session_id:'%s', leo_id:'%s', why:'%s'" % (session_id, leo_id, e))
            return False
        # get info from seraph
        try:
            d_collect = seraph_client.checkUserCollect(user_id, [leo_id])
            self._logging.info("leo:'%s', logined:'%s', collection:'%s'" % (leo_id, is_login, d_collect))
            return d_collect[leo_id]
        except TIOError as e:
            self._logging.warn("exception caught whle checking user collect, session_id:'%s', leo_id:'%s', TIOError why:'%s'" % (session_id, leo_id, e))
            return False
        except Exception as e:
            self._logging.warn("exception caught while checking user collect, session_id:'%s', leo_id:'%s', why:'%s'" % (session_id, leo_id, e))
            return False

    def _get_sell_status(self, sku_id):
        sku = warehouse_client.getSku(int(sku_id), ['sell_status'], [], use_cache=False)
        try:
            return int(sku.fields['sell_status'])
        except Exception as e:
            self._logging.error("exception caught while getting sell_status, sku_id:'%s', exc:'%s'" % (sku_id, e))
            return -1

    def _refine_x_num_per_oneshot(self, target_object):
        # max
        max_num_per_oneshot = self._DEFALUT_MAX_NUM_PER_ONESHOT
        if target_object.max_num_per_oneshot not in (None, '', -1):
            max_num_per_oneshot = target_object.max_num_per_oneshot
        if target_object.stocks not in (None, '', -1) and target_object.stocks < max_num_per_oneshot:
            max_num_per_oneshot = target_object.stocks
        # min
        min_num_per_oneshot = max(target_object.min_num_per_oneshot or 0, self._DEFALUT_MIN_NUM_PER_ONESHOT)
        return max_num_per_oneshot, min_num_per_oneshot

    def _process_sell_restriction(self, leo):
        sell_restriction = {}
        sell_restriction['sell_status'] = self._get_sell_status(leo._sku['id'])

        # x num per oneshot
        xmax, xmin = self._refine_x_num_per_oneshot(leo)
        sell_restriction['max_num_per_oneshot'] = xmax
        sell_restriction['min_num_per_oneshot'] = xmin

        # fixbug: base sku no max_num_per_oneshot
        if sell_restriction['max_num_per_oneshot'] == -1 and len(leo.resources) > 0:
            max_num_per_oneshot = leo.resources[0].max_num_per_oneshot
            sell_restriction['max_num_per_oneshot'] = max_num_per_oneshot

        return sell_restriction

    def _leo_total_sell_restriction(self, leo, leo_detail):
        sku_representation = leo_detail.get('sku_representation', None)
        sell_restriction = leo_detail.get('sell_restriction', None)
        if not (sku_representation and sell_restriction):
            return

        represent_type = sku_representation['represent_type']
        if represent_type == 'list':
            sell_map = {'1':0, '2':0, '3':0, '4':0}
            represent_data = sku_representation['represent_data']
            sell_count = len(represent_data)

            # have sku_representation, but no sku
            # status is stop sell
            if sell_count is 0:
                sell_restriction['sell_status'] = 3
                return
            
            # merge all sku sell status
            for sku in represent_data:
                sell_status = sku['sell_status']
                sell_map[str(sell_status)] += 1

            # merge rule:
            # 1. has sell sku
            if sell_map['2'] > 0:
                new_sell_status = 2
            # 2. all presell
            elif sell_map['1'] == sell_count:
                new_sell_status = 1
            # 3. all stop sell
            elif sell_map['3'] == sell_count:
                new_sell_status = 3
            # 4. all sellout
            elif sell_map['4'] == sell_count:
                new_sell_status = 4
            # 5. has presell sku
            elif sell_map['1'] > 0:
                new_sell_status = 1
            # 6. has stop sell
            elif sell_map['3'] > 0:
                new_sell_status = 3
            # 7. other sellout
            else:
                new_sell_status = 4
        sell_restriction['sell_status'] = new_sell_status

    def _leo_detail_comm_info(self, leo, leo_detail):
        # update leo total sell status
        self._leo_total_sell_restriction(leo, leo_detail)
        leo_detail['city'] = leo.city or ''

    def _leo_detail_101(self, leo, extra_params):
        def _inner_get_resource_specified_props(leo_id, res_obj, res_type):
            """get specified props from resource.
            """
            ret = {}
            if res_type not in self._category_specified_props_map:
                self._logging.error("leo:'%s', unsupported resource type:'%s' from:'%s'" % (leo_id, res_type, res_obj))
                return ret
                
            props = self._category_specified_props_map.get(res_type)
            if not props:
                return ret

            for p in props:
                ret[p] = self._gattr(res_obj, p, f=str, default='')
            return ret

        # start
        ret = {}
        ret['template_id'] = self._gen_template_id(leo)
        ret['mapicon'] = self.mapicon.get_mapicon(leo._category.id)
        ret['category'] = dict(cn_name=leo._category.cn_name, id=leo._category.id, icon_view=self.mapicon.getDetailCategoryIcon(leo._category.id))
        ret['name'] = leo.cn_name or leo._sku['cn_name'] or leo.main_title
        ret['title'] = leo.cn_name or leo._sku['cn_name'] or leo.main_title
        ret['days'] = leo.days or -1
        ret['sell_price_unit'] = leo.sell_price_unit or ''
        ret['leo_target_type'] = leo.target_type
        ret['leo_target_id'] = int(leo.target_id)
        ret['time'] = self._process_time(leo)
        ret['related_id'] = leo.related_id or ''
        ret['is_bonus_available'] = bool(leo.is_bonus_available)
        ret['advance_book_day'] = leo.advance_book_day or 0
        ret['child_count'] = leo.child_count or 0
        ret['adult_count'] = leo.adult_count or 0
        ret['is_can_book'] = bool(leo.is_can_book)
        ret['resource_type'] = leo.resource_type or 0
        #ret['pay_mode'] = leo.pay_mode or self._DEFAULT_PAY_MODE
        ret['pay_method_list'] = self._get_pay_methods(leo.biz_id)
        ret['sell_restriction'] = self._process_sell_restriction(leo)
        ret['images'] = leo.images
        ret['tags'] = [ dict(name=i.name, id=i.id) for i in leo.tags if i.id not in self.exclusive_tag_ids ] if leo.tags else []

        ret['server_biz_name'] = leo.server_biz_name or ''
        ret['poi'] = leo.poi or leo.server_biz_name or ''
        ret['address'] = leo.address or ''

        # time price
        l_time_prices = warehouse_client.getTimePriceList(int(leo.target_id))
        ret['time_price'] = [i.__dict__ for i in l_time_prices]
        ret['min_price'] = leo.min_price or leo.quoted_price or leo.advice_min_price or 0
        ret['origin_price'] = self._origin_price(leo.quoted_price)
        ret['providers'] = ret['provider'] = self._provider(leo.server_biz_name, leo.source_id)

        basic_services = []
        ret['services'] = {
            'basic': basic_services,
            'others':leo.other_services or []
        }

        # resources
        ret['resources'] = []
        for r in leo.resources:
            res_detail = {}
            ret['resources'].append(res_detail)

            # fields
            res_detail['category'] = r._category.name
            res_detail['category_id'] = r._category.id
            res_detail['name'] = r.cn_name
            res_detail['sku_refer_id'] = r.id

            l_refer_props = {'contain_type':('int', -1), 'contain_count':('int', -1), 'related_id':('int', -1)}
            for p,restrict in l_refer_props.items():
                value_type, value_default = restrict[0], restrict[1]
                prop_val = r._extra_data.get(p) if r._extra_data.has_key(p) else value_default
                self._logging.debug("leo:'%s', before converting, prop:'%s', value:'%s', raw type:'%s'" % (leo.id, p, prop_val, type(prop_val)))
                # convert to required type
                prop_val = self._convert_value_with_type(prop_val, value_type) if prop_val else value_default
                self._logging.debug("leo:'%s', after converting, prop:'%s', value:'%s', raw type:'%s'" % (leo.id, p, prop_val, type(prop_val)))
                # ok
                res_detail[p] = prop_val

            res_detail['location'] = dict(lat=r.lat, lon=r.lon)
            res_detail['resource_product_name'] = r.resource_product_name or ''
            res_detail['address'] = r.address or ''
            res_detail['open_time'] = r.open_time or ''
            # res_detail['origin_price'] = r.quoted_price or 0
            res_detail['user_days'] = r.user_days or '0'
            res_detail['ticket_place'] = r.ticket_place or ''
            res_detail['specified_props'] = _inner_get_resource_specified_props(leo.id, r, r._category.name )

            # NOTICE: handle address, only use 'hotel' address for package if exists
            if r._category.name == 'hotel':
                ret['address'] = r.address or ''
                ret['server_biz_name'] = r.cn_name
                # TODO in lms, set for outer ret
                services = ['room', 'breakfast', 'dinner', 'buffet', 'afternoon_tea']
                for sname in services:
                    x = self._gattr(r, sname, default=None)
                    if x:
                        basic_services.append( self._conv(x, f=json.loads) )

        ret['biz_phone'] = leo.biz_phone or leo.consult_phone or ''
        ret['biz_website'] = leo.biz_website or ''
        ret['consult_phone'] = leo.consult_phone or leo.biz_phone or ''
        ret['lrzm_tips'] = self._compose_lrzm_tips(leo, extra_params['v'])
        ret['description'] = self._compose_desc(leo, extra_params['v'], self._get_desc(leo.id), ret['lrzm_tips'])
        ret['booking_policy'] = self._conv(leo.booking_policy or '[]', f=json.loads)
        ret['ticket_usage'] = self._conv(leo.ticket_usage or '[]', f=json.loads)
        ret['ticket_rule'] = self._conv(leo.ticket_rule or '[]', f=json.loads)

        lat = leo.lat or 0.0
        lon = leo.lon or 0.0
        ret['location'] = dict(lat=lat, lon=lon)

        # finally
        
        return ret

    def getTimePriceList(self, leo_id, sku_id, book_time):
        price_list = warehouse_client.getTimePriceList(sku_id, book_time)
        # old version not leo_id
        if not leo_id:
            return price_list

        try:
            self._logging.info("get leo:%s", leo_id)
            leo = warehouse_client.getLeoV2(leo_id)
        except Exception as e:
            self._logging.error("exception caught while get leo:'%s', exc:'%s'" % (
                leo_id, e))
            return price_list

        pa = ProductAssembly(None)
        pa.price_calendar(leo, sku_id=sku_id, price_calendar=price_list)
        return price_list

    def getImageList(self, target_type, target_id):
        return warehouse_client.getImageList(target_type, target_id)

    def _compose_range(self, dict_target, key, range_start, range_end, restriction=''):
        dict_target[key] = value = {}
        value['type'] = 'range'
        value['value'] = [range_start, range_end]
        value['restriction'] = restriction

    def _compose_enum(self, dict_target, key, list_enum_value, restriction=''):
        dict_target[key] = value = {}
        value['type'] = 'enum'
        value['value'] = list_enum_value
        value['restriction'] = restriction

    def _compose_fill(self, dict_target, key, def_fill_value='', restriction=''):
        dict_target[key] = value = {}
        value['type'] = 'fill'
        value['value'] = def_fill_value
        value['restriction'] = restriction

    def _compose_trans_params(self, leo):
        # NOTICE: hard-code now
        ret = {}
        ret['contacter_info'] = user_info = {}
        self._compose_fill(user_info, 'phone')
        self._compose_fill(ret, 'quantity')
        self._compose_fill(user_info, 'contactor_name')
        return ret

    def _compose_sku_representation(self, leo):
        ret = {}

        ################################################################
        # CRITICAL: code between ######... is just for android client *BUG*. can be removed
        ################################################################
        x = self._process_sell_restriction(leo)
        ret.update(x)
        ################################################################

        def _from_barebone(leo):
            ret = {}
            return ret

        def _from_sku(leo):
            ret['represent_type'] = 'list'
            ret['represent_data'] = represent_data = []
            item = {}
            represent_data.append(item)
            # do composing
            sku_id = leo._sku.get('id') or '0'
            item['time'] = self._process_time(leo)
            item['sell_status'] = self._get_sell_status(str(sku_id))
            item['price'] = leo.min_price or leo.quoted_price or leo.advice_min_price or 0
            item['origin_price'] = self._origin_price(leo.quoted_price)
            item['price_info'] = leo.price_info or ''
            item['title'] = leo._sku.get('cn_name') or ''
            item['sku_id'] = str(sku_id)

            xmax, xmin = self._refine_x_num_per_oneshot(leo)
            item['max_num_per_oneshot'] = xmax
            item['min_num_per_oneshot'] = xmin
            return ret

        def _from_goods(leo):
            ret = {}
            ret['represent_type'] = 'list'
            ret['represent_data'] = represent_data = []
            return ret

        def _from_refers(leo):
            ret = {}
            ret['represent_type'] = 'list'
            ret['represent_data'] = represent_data = []
            for r in leo.resources:
                item = {}
                represent_data.append(item)
                # do composing
                sku_id = r.id or r._sku.get('id') or '0'
                item['time'] = self._process_time(r)
                item['sell_status'] = self._get_sell_status(str(sku_id))
                item['price'] = r.min_price or r.quoted_price or r.advice_min_price or 0
                item['origin_price'] = r.quoted_price or 0
                item['price_info'] = r.price_info or ''
                item['title'] = r.cn_name or r._sku.get('cn_name') or ''
                item['sku_id'] = str(sku_id)
                xmax, xmin = self._refine_x_num_per_oneshot(r)
                item['max_num_per_oneshot'] = r.max_num_per_oneshot
                item['min_num_per_oneshot'] = r.min_num_per_oneshot
            return ret

        def _from_spu(leo):
            ret = {}
            ret['represent_type'] = 'list'
            ret['represent_data'] = represent_data = []
            return ret

        # main part, calls specific handler for different targets
        leo_target_type = leo.target_type
        from_handler = ''.join(('_from_', leo_target_type, '(leo)'))
        try:
            self._logging.info("getting representation using from handler:'%s'" % from_handler)
            return eval(from_handler)
        except NameError as e:
            self._logging.error("no sku representation handler named:'%s'" % from_handler )
            return {}

    def api(self, start, end, appkey, version, pageNo, pageSize, sign):
        '''
        provide api for get leos
        '''
        api_result = {}
        #判断appkey                                                             
        if not appkey == "ANAVI":
            api_result["error"] = 102
            api_result["message"] = "appkey有误"
            return api_result
        else:
            #高德约定：参数生成sign时按照字母升序排列
            url_str = str(end) + str(pageNo) + str(pageSize) + str(start) + version + "&" + appkey
            real_sign = unicode_to_md5(url_str)
            #判断sign
            if sign == real_sign:
                try:
                    #获取rows
                    now_time = time.localtime(time.time())
                    today_date = time.strftime('%Y%m%d',now_time)
                    api_result["pagesize"] = pageSize
                    api_result["version"] = today_date
                    api_result["error"] = 0
                    api_result["message"] = "获取成功"
                    leo_list = self.amap_get_leo(pageNo, pageSize)
                    result = self.amap_build_row(leo_list)
                    api_result["results"] = result
                    return api_result
                except Exception,e:                                             
                    self._logging.error(e)
                    api_result['error'] = 1
                    api_result['message'] = '无数据。接口变动，请联系懒人周末的同学。'
                    api_result['rows'] = []                                     
                    return api_result                                           
            else:
                api_result["error"] = 101                                       
                api_result["message"] = "鉴权失败（sign值不相同）"              
                return api_result

    def amap_get_leo(self, page_number, page_count):
        """
        取warehouse的数据
        """
        try:
            leo_list = warehouse_client.getLeosOnePageV2(page_index=page_number, n_items_per_page=page_count, leak_status = ["Audited"])
            return leo_list
        except Exception, e:
            self._logging.error(e)

    def amap_build_row(self, leo_list):
        """
        将活动添加至rows
        """
        rows = []
        for i in range(0, len(leo_list)):
            row = {}
            row["id"] = leo_list[i].id
            row["title"] = leo_list[i].cn_name
            if leo_list[i].images:                                  
                row["image"] = leo_list[i].images[0]
            else:
                row["image"] = "http://lanrenzhoumo.com/images/screen.png"
            row["author"] = "懒人发布"
            row["source"] = "懒人周末"
            row["summary"] = "更多惊喜请戳http://lanrenzhoumo.com"
            if leo_list[i].id:
                leo_id = int(leo_list[i].id)                        
                des = json.loads(warehouse_client.getDescription(target_type='leo', target_id=leo_id))
                if des:
                    row['content']=''
                    for des_one in des:                                 
                        row['content'] += des_one.get('content')        
                        row['content'] += '\r\n'
                else:
                    row["content"]="啊哦，此活动暂无描述。关注微信公众号lanrenzhoumo获取更多小道消息。"
            rows.append(row)
        return rows

    def getCategoryTree(self):
        try:
            cats = warehouse_client.getCategoryTree()
            cats = json.loads(cats)
        except TIOError as e:
            self._logging.warn("failed to get category")
            return None
        except Exception as e:
            self._logging.warn("except caught while getting category")
            return None
        ret, orders = [], cats['SHOW_ORDER']

        def __inner_gc(children_node):
            """
            recursively get category from tree
            @children_node: children node represents all data.
            """
            if 'SHOW_ORDER' not in children_node:
                return None

            ret = []
            # adjust show orders
            # sos = children_node['SHOW_ORDER']
            sos = [ 'all'
                    ,'diy'
                    , 'bar'
                    , 'music'
                    , 'drama'
                    , 'exhibition'
                    , 'food'
                    , 'shopping'
                    , 'movie'
                    , 'party'
                    , 'sport'
                    , 'charity'
                    , 'business'
                ]

            for cat_name in sos:
                cur_node = children_node[cat_name]
                cself, cchildren = cur_node.get('self', {}), cur_node.get('children', {})
                c = dict( name=cat_name
                          , cn_name=cself.get('cn_name', None)
                          , icon_view=cself.get('icon_view', None)
                          , icon_pressed=cself.get('icon_pressed', None)
                          , description=cself.get('description', None)
                          , children=[]
                )
                c['children'] = __inner_gc(cchildren) or []
                ret.append( c )
            return ret

        return __inner_gc(cats)

    def __getLeosOnePage(self, session_id, page_index, n_items_per_page, category_name, __enc__):
        """ just a demo of getLeoV2
        """
        ret = {}
        leos = warehouse_client.getLeos(page_index, n_items_per_page, category_name)
        ret['is_final_page'] = (len(leos) < n_items_per_page)

        ret['leos'] = ret_leos = []
        for leo in leos:
            mod_leo_target_id, mod_leo_id = leo.id, leo.target_id
            if __enc__ != 'zmkm':
                enc_data = self.encryta.encrypt(leo.id, 0)
                if enc_data['ok']:
                    mod_leo_id = enc_data['data']
                else:
                    self._logging.error("failed to encryt leo id:'%s' caz: '%s'" % (leo.id, enc_data['why']))
                    continue
                # allow encrypt failure for target_id
                enc_data = self.encryta.encrypt(leo.target_id, 0)
                if enc_data['ok']:
                    mod_leo_target_id = enc_data['data']
                else:
                    self._logging.warn("failed to encrypt leo:'%s' target id:'%s'" % (leo.id, leo.target_id))

            item = {}
            item['collected'] = self._is_leo_been_collected_by_user(leo.id, session_id)
            item['leo_id'] = mod_leo_id
            item['cn_name'] = leo.cn_name
            item['tag'] = [i.name for i in leo.tags]
            item['images'] = [leo.images[0] if leo.images else ""] # for extending.
            item['biz_phone'] = leo.biz_phone or leo.consult_phone or ''
            item['address'] = leo.address or ''
            item['biz_website'] = leo.biz_website or ''
            item['address'] = leo.address
            item['poi'] = leo.poi
            item['category'] = {'name':category_name,'cn_name':leo._category.cn_name, 'icon_view':leo._category.icon_view}
            item['title'] = leo.main_title or leo.sub_title
            item['target'] = {'type':leo.target_type, 'id':mod_leo_target_id}
            item['time_desc'] = leo.time_desc
            # sell-related stuff
            item['participate_status'] = leo.participate_status
            item['price'] = { 'sell':leo.min_price or leo.sell_price or 0,
                              'origin':leo.quoted_price or leo.min_price or leo.sell_price or 0 }
            item['sell_status'] = leo.sell_status
            if leo.target_type == g_wh_db_info.LEO_TARGET_TYPE_SKU:
                item['sell_status'] = self._get_sell_status(leo.target_id)

            # more
            # time_info
            # distance

            ret_leos.append(item)
        ret['leos_count'] = len(ret_leos)
        return ret

    def getLeoIdsByFilter(self, page_index, n_items_per_page, category_name='', keyword='', city=''):
        try:
            return warehouse_client.getLeoIds(page_index,n_items_per_page,category_name,keyword,city=city,order_rule='time_desc')
        except TIOError as e:
            self._logging.warn("exc caught while getting leo ids category:'%s', keyword:'%s', page_index:'%s', exc:'%s'" % (category_name, keyword, page_index, e))
            return []
        except TIllegalArgument as e:
            self._logging.warn("exc caught while getting leo ids category:'%s', keyword:'%s', page_index:'%s', exc:'%s'" % (category_name, keyword, page_index, e))
            return []

