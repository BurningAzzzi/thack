#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Date  : 2014-0828
# Author: zhizhimama
# Email : zhima@meishixing.com
"""
leo dev config
"""
from cache_config_dev import *

LOCAL_ADDRESS = '127.0.0.1'

DB_PORT = 6033
DB_HOST = '115.236.23.187:6033'
DB_DATABASE = 'leo_dev'
DB_USER = 'root'
DB_PASSWORD = 'shuotao1234!@#$shuotao'

TAILOR_DB_PORT = 6033
TAILOR_DB_HOST = '115.236.23.187:6033'
TAILOR_DB_DATABASE = 'tailor'
TAILOR_DB_USER = 'root'
TAILOR_DB_PASSWORD = 'shuotao1234!@#$shuotao'

MONGO_DB_PORT = 27017
MONGO_DB_HOST = '115.236.23.187'
MONGO_DB_DATABASE = 'leo_dev'
MONGO_DB_USER = ''
MONGO_DB_PASSWORD = ''

AMQP_VHOST = "debug"

SPUFS_IMAGE_CNF = {
    'root': '/home/meishixing/panda_media/image_dev/leo',
    'urlbase': '/'
    }


ERROR_LOG_PATH = '../error.log'

RPC_SERVER_ADDRESS = (LOCAL_ADDRESS, 9091)

SERAPH_PORT = 9121
SERAPH_RPC_ADDRESS = LOCAL_ADDRESS
TRANS_PORT = 9111
TRANS_RPC_ADDRESS = LOCAL_ADDRESS
WAREHOUSE_PORT = 9131
WAREHOUSE_RPC_ADDRESS = LOCAL_ADDRESS
USOPP_PORT = 3333
USOPP_RPC_ADDRESS = LOCAL_ADDRESS

SPUMASTER_ADDRESS = ''

COUNT_SERVER_CONFIG = {
    'host': LOCAL_ADDRESS,
    'port': 6380,
    'db': 1
    }

BAADE_HOST = "http://localhost:11100"
SE_HOST='127.0.0.1'
SE_PORT=9999

# rtc config
RTC_CNF = {
    'TCSightPaPlugin': {
    'rtc_base_url': 'http://218.244.137.196:22310',
    'aml_debug': True,
    }
    }

# dev版本密钥
RONGCLOUD_APP_KEY = 'kj7swf8o7cd32'
RONGCLOUD_APP_SECRET = '7QYT0qUJHZ'