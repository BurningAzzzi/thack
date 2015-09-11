#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Date  : 2014-08-28
# Author: zhizhimama
# Email : zhima@meishixing.com

"""
dynamic gen config vars
"""
import sys
import os
import logging
from tornado.options import define, options, parse_command_line, enable_pretty_logging
import sputnik.SpuConfig as SpuConfig

def to_debug(address):
    if 'com' not in address:
        return address
    index = address.find('.')
    return address[:index] + '.debug' + address[index:]

configfile = sys.argv[-1]
dirname, basename = os.path.split(configfile)
module_name = basename.split('.')[0]
sys.path.append(dirname)
cm = __import__(module_name)

define("server_port", default=None, help="run on the given server port", type=int)
define("app_port", default=None, help="run on the given application port", type=int)
define("debug", default=False, help="debug", type=bool)
define("tongcheng_api_test", default=None, help="Use tongcheng test api", type=bool)
parse_command_line()

DEBUG = options.debug
if DEBUG:
    cm.WAREHOUSE_RPC_ADDRESS = to_debug(cm.WAREHOUSE_RPC_ADDRESS)
    cm.SERAPH_RPC_ADDRESS = to_debug(cm.SERAPH_RPC_ADDRESS)
    cm.TRANS_RPC_ADDRESS = to_debug(cm.TRANS_RPC_ADDRESS)

VC_REDIS_CONF = cm.VC_REDIS_CONF

# logging config
logging_config = {
    'log_slow' : True,
    'log_slow_time' : 1000,
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

APP_PORT = options.app_port

spusys_config = {
    'enable': True,
    'spumaster_server_addr': cm.SPUMASTER_ADDRESS,
    'app_port': APP_PORT,
    'http_thread': False,
    'network_interface': cm.LOCAL_ADDRESS,
    }
from sputnik import sputnik_init
if DEBUG:
    logging.getLogger().setLevel(logging.DEBUG)
else:
    logging.getLogger().setLevel(logging.INFO)


sputnik_init(logging_config,
             spusys_config=spusys_config,
             debug=DEBUG
             )
from sputnik.SpuFieldFilter import SpuFieldFilter
from sputnik.SpuDB import SpuDB_Tornado
from sputnik.Sputnik import set_logging_config
from sputnik.SpuDB import SpuDBManager, SpuDBCreateDB, SpuMongodb
from sputnik.SpuContext import SpuContext
from sputnik.SpuDBObject import *
from sputnik.SpuUOM import SpuUOM
from sputnik.SpuFS import *
from sputnik.SpuDebug import *
from sputnik.SpuFactory import *
from sputnik.SpuRequest import SpuRequestHandler

# global config
SpuConfig.SpuDebug = DEBUG
SpuFieldFilter.debug = DEBUG
SPUFS_IMAGE_CNF = cm.SPUFS_IMAGE_CNF
version = 0.1

# database config
DBCNF = {
    'dbtype' : SpuDB_Tornado,
    'host' : cm.DB_HOST,
    'port' : cm.DB_PORT,
    'database' : cm.DB_DATABASE,
    'user' : cm.DB_USER,
    'passwd' : cm.DB_PASSWORD,
    'debug' : DEBUG
    }

RONGCLOUD_APP_KEY = cm.RONGCLOUD_APP_KEY
RONGCLOUD_APP_SECRET = cm.RONGCLOUD_APP_SECRET

# mogodb config
MONGO_DBCNF = {
    'host' : cm.MONGO_DB_HOST,
    'port' : cm.MONGO_DB_PORT,
    'database' : cm.MONGO_DB_DATABASE,
    'user' : cm.MONGO_DB_USER,
    'passwd' : cm.MONGO_DB_PASSWORD,
    'debug' : DEBUG
    }

# rpc service
RPC_SERVER_ADDRESS = cm.RPC_SERVER_ADDRESS
SERAPH_RPC_ADDRESS = (cm.SERAPH_RPC_ADDRESS, cm.SERAPH_PORT)
WAREHOUSE_RPC_ADDRESS = (cm.WAREHOUSE_RPC_ADDRESS, cm.WAREHOUSE_PORT)
SE_RPC_ADDRESS = (cm.SE_HOST, cm.SE_PORT)
TRANS_RPC_ADDRESS = (cm.TRANS_RPC_ADDRESS, cm.TRANS_PORT)
USOPP_RPC_ADDRESS = (cm.USOPP_RPC_ADDRESS, cm.USOPP_PORT)

start_sputnik_logging(error_log_path=cm.ERROR_LOG_PATH)

COUNT_SERVER_CONFIG = cm.COUNT_SERVER_CONFIG

BAADE_HOST = cm.BAADE_HOST

# rtc config
RTC_CNF = cm.RTC_CNF

#geo offset service
suggest_address = 'http://%s:%s' % ('115.236.23.187', '58001')
