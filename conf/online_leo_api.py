#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Date  : 2014-0828
# Author: zhizhimama
# Email : zhima@meishixing.com
"""
leo online config
"""
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
from cache_config_online import *

DB_ADDRESS = 'db_1'

DB_PORT = 6033
DB_HOST = DB_ADDRESS
DB_DATABASE = 'leo_online'
DB_USER = 'leo'
DB_PASSWORD = 'leo'

MONGO_DB_PORT = 27017
MONGO_DB_HOST = DB_ADDRESS
MONGO_DB_DATABASE = 'leo_online'
MONGO_DB_USER = ''
MONGO_DB_PASSWORD = ''
AMQP_VHOST = "debug"

SPUFS_IMAGE_CNF = {
    'root': '/home/meishixing/panda_media/image_online/leo',
    'urlbase': '/'
    }
ERROR_LOG_PATH = '/alidata1/logs/error_online/leo_api.log'

RPC_SERVER_ADDRESS = ('leo.panda_service.com', 8880)

RPC_PORT = 8880
WAREHOUSE_PORT = 8980
WAREHOUSE_RPC_ADDRESS = 'online.warehouse.com'
TRANS_PORT = RPC_PORT
TRANS_RPC_ADDRESS = 'online.trans.com'
SERAPH_PORT = RPC_PORT
SERAPH_RPC_ADDRESS = 'online.seraph.com'
USOPP_PORT = RPC_PORT
USOPP_RPC_ADDRESS = 'online.usopp.com'

SPUMASTER_ADDRESS = 'service_warehouse_1:9280'

COUNT_SERVER_CONFIG = {
    'host': 'cache_1',
    'port': 6385,
    'db': 1
    }

BAADE_HOST = "http://api.online.group.meishixing.com/"
SE_HOST='online.search.com'
SE_PORT=8990

# rtc config
RTC_CNF = {
    'TCSightPaPlugin': {
    'rtc_base_url': 'http://online.rtc.com:8880',
    'aml_debug': True,
    }
    }

TAILOR_DB_PORT = 6033
TAILOR_DB_HOST = 'db_1'
TAILOR_DB_DATABASE = 'tailor_online'
TAILOR_DB_USER = 'leo'
TAILOR_DB_PASSWORD = 'leo'

# online版本密钥
RONGCLOUD_APP_KEY = 'qf3d5gbj3ilwh'
RONGCLOUD_APP_SECRET = 'UOjHGQq1qZ4C'

OSS_DIR = "leo_comment"
