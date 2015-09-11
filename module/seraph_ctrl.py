#!/usr/bin/env python
#coding:utf8

from sputnik.SpuLogging import *
from module.base_ctrl import SERAPH_RPC_ADDRESS

from seraph.ttypes import *
from seraph_client import SeraphClient

SpuLogging.info("\tRPC seraph address:%s,\t port:%s" % (SERAPH_RPC_ADDRESS[0], SERAPH_RPC_ADDRESS[1]))
seraph_client = SeraphClient()
seraph_client.connect(SERAPH_RPC_ADDRESS)


def get_biz(biz_id):
    try:
        return seraph_client.getBiz(long(biz_id))
    except TIOError as e:
        SpuLogging.error("no such biz, id:'%s', exc:'%s'" % (biz_id, e))
        return None
    except Exception as e:
        SpuLogging.error("unexpected error occurs, check it out, exc:'%s'" % e)
        return None

def get_user(user_id):
    try:
        return seraph_client.getUserLeo(long(user_id))
    except TIOError as e:
        SpuLogging.error("no such user, id:'%s', exc:'%s'" % (user_id, e))
        return None
    except Exception as e:
        SpuLogging.error("unexpected error occurs, check it out, exc:'%s'" % e)
        return None

def get_collectors(leo_id, page_index=0, n_per_page=10):
    try:
        return seraph_client.getCollectors(long(leo_id), page_index, n_per_page)
    except TIllegalArgument as e:
        SpuLogging.warn("invalid arguments:'%s'" % e)
        return None
    except Exception as e:
        SpuLogging.warn("seraph error:'%s'" % e)
        return None

def get_biz_info(biz_id):
    '''get biz info by biz_id'''
    try:
        return seraph_client.getBizInfoByBasicId(biz_basic_id=biz_id)
    except TIllegalArgument as e:
        SpuLogging.error("invalid arguments:{} where biz_id={}".format(e, biz_id))
    except Exception as e:
        SpuLogging.error("seraph error:{} where biz_id={}".format(e, biz_id))
