"""week event"""
# -*- coding: utf-8 -*-
#
# Copyright 2013 meishixing.com
# Copyright 2014 lanrenzhoumo.com
# by biluochun@meishixing.com
# 2014-12-10
#

import json
import time
from usopp_ctrl import usopp_client
from sputnik.SpuLogging import SpuLogging

_LOGGING = SpuLogging(module_name='week_event')

def weekend_event(event_id, lat, lon):
    # by zhima , error when exception catched
    leos = []
    try:
        leos = usopp_client.getActivityLeos(event_id, lat, lon)
        leos = json.loads(leos.rst)
    except Exception as m:
        _LOGGING.error('weekend_event failed lat:%s lon:%s msg:%s',
                       lat, lon, m)
    return leos
