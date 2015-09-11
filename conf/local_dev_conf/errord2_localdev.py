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

DEBUG = True
APP_PORT = 14011

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

LOGGING_CONFIG = {
    'log_slow' : False,
    'log_slow_time' : 500,
    'log_function' : {
        'all' : True,
        'flowpath' : {
            'all' : True,
            'flowpath' : True,
            'logic' : True,
            'service' : True,
            'db' : True,
            'cache' : True
            },
        'perf' : {
            'all' : True,
            'perf' : True,
            'func' : True,
            'service' : True,
            'db' : True,
            'cache' : True
            }
        }    
    }


SPUFS_IMAGE_CNF = {
    'root': '/home/meishixing/panda_media/image_dev/leo',
    'urlbase': '/'
    }


ERROR_LOG_PATH = '../error.log'

RPC_SERVER_ADDRESS = ('localhost', 9091)

SERAPH_RPC_ADDRESS = ('localhost', 9121)
TRANS_RPC_ADDRESS = ('localhost', 9111)
WAREHOUSE_RPC_ADDRESS = ('localhost',9101)

# dev版本密钥
RONGCLOUD_APP_KEY = 'kj7swf8o7cd32'
RONGCLOUD_APP_SECRET = '7QYT0qUJHZ'