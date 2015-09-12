#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
# Date  : 2015-09-11
# Author: Master Yumi
# Email : yumi@meishixing.com


import sys
import tornado
import tornado.httpserver
import tornado.ioloop
import tornado.web
sys.path.insert(0, 'api')
from config import *
from sputnik.SpuDebug import is_debug
    

def init():
    createSpuFS('spuFS', SPUFS_IMAGE_CNF)

    db = SpuDBCreateDB(DBCNF)
    dbc = db.create()
    dbc.set_charset('utf8mb4')
    dbc.connection()
    SpuDBManager.add_spudb(dbc)

    SpuContext.init_context(dbc, None)

    SpuDOFactory.init_factory(DEBUG)
    SpuUOM.import_module("sku")
    SpuUOM.import_module("message")
    SpuUOM.import_module("mark")
    SpuUOM.import_module("im")
    SpuUOM.import_module("user")
    SpuUOM.import_module("test")
    SpuUOM.import_module("route")
    SpuUOM.import_module("resource")
    SpuUOM.load()

def start():
    class Application(tornado.web.Application):
        def __init__(self):
            if DEBUG:
                doc = True
            else:
                doc = False
            handlers = SpuUOM.url_rule_list(doc)
            settings = dict(
                service_title=u"Thack",
                template_path=os.path.join(os.path.dirname(__file__), "templates"),
                static_path=os.path.join(os.path.dirname(__file__), "static"),
                )
            tornado.web.Application.__init__(self, handlers, debug=DEBUG, **settings)

    http_server = tornado.httpserver.HTTPServer(Application(), xheaders = True)
    SpuLogging.info("start success")
    http_server.listen(APP_PORT)
    tornado.ioloop.IOLoop.instance().start()


def print_db_info():
    SpuLogging.info("DB Info:")
    SpuLogging.info("\tDB Type:%s" % DBCNF['dbtype'])
    SpuLogging.info("\tDB Host:%s" % DBCNF['host'])
    SpuLogging.info("\tDB Port:%s" % DBCNF['port'])
    SpuLogging.info("\tDB Database:%s" % DBCNF['database'])

def print_sys_info():
    SpuLogging.info("Tornado Version: %s" % tornado.version)
    SpuLogging.info("Application Port:%s" % APP_PORT)
    SpuLogging.info("Debug Mod:%s" % DEBUG)

def usage():
    print "usage: ./leo.py [--option=value] configfile [--dev]"
    print "\t --dev\t\tno install Module"

def main():
    init()
    print_sys_info()
    print_db_info()
    start()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        usage()
        sys.exit(0)
    main()
