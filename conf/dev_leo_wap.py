#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Date  : 2014-0828
# Author: zhizhimama
# Email : zhima@meishixing.com
"""
leo dev config
"""
LEVEL = 'dev'
from wap_session_config_dev import *
from cache_config_dev import *

import socket
import fcntl
import struct

# NOTICE to temporary change local ip, not appropriate to do this .    linux only
def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])

LOCAL_ADDRESS = get_ip_address('eth0')
DB_ADDRESS = 'db_1'

DB_PORT = 6033
DB_HOST = DB_ADDRESS
DB_DATABASE = 'leo_{}'.format(LEVEL)
DB_USER = 'leo'
DB_PASSWORD = 'leo'

MONGO_DB_PORT = 27017
MONGO_DB_HOST = DB_ADDRESS
MONGO_DB_DATABASE = 'leo_{}'.format(LEVEL)
MONGO_DB_USER = ''
MONGO_DB_PASSWORD = ''
AMQP_VHOST = "debug"

SPUFS_IMAGE_CNF = {
    'root': '/home/meishixing/panda_media/image_{}/leo'.format(LEVEL),
    'urlbase': '/'
    }
ERROR_LOG_PATH = '/alidata1/logs/error_{}/leo_wap.log'.format(LEVEL)
RPC_PORT = 8880
WAREHOUSE_RPC_ADDRESS = '{}.warehouse.com'.format(LEVEL)
WAREHOUSE_PORT = 8980
TRANS_RPC_ADDRESS = '{}.trans.com'.format(LEVEL)
TRANS_PORT = RPC_PORT
SERAPH_RPC_ADDRESS = '{}.seraph.com'.format(LEVEL)
SERAPH_PORT = RPC_PORT
USOPP_RPC_ADDRESS = '{}.usopp.com'.format(LEVEL)
USOPP_PORT = RPC_PORT

SPUMASTER_ADDRESS = 'dev_1:9284'

COUNT_SERVER_CONFIG = {
    'host': 'cache_1',
    'port': 6380,
    'db': 1
    }

API_ADDRESS = 'http://api.{}.lanrenzhoumo.com'.format(LEVEL)
SE_HOST='127.0.0.1'
SE_PORT=9999
# rtc config
RTC_CNF = {
    'TCSightPaPlugin': {
    'rtc_base_url': 'http://218.244.137.196:22310',
    'aml_debug': True,
    }
    }

TAILOR_DB_PORT = 6033
TAILOR_DB_HOST = 'db_1'
TAILOR_DB_DATABASE = 'tailor_dev'
TAILOR_DB_USER = 'leo'
TAILOR_DB_PASSWORD = 'leo'

# dev版本密钥
RONGCLOUD_APP_KEY = 'kj7swf8o7cd32'
RONGCLOUD_APP_SECRET = '7QYT0qUJHZ'