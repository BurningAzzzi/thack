#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Date   : 2014-08-15
# Author : Master Yumi
# Email  : yumi@meishixing.com

from sputnik.SpuLogging import *
from module.base_ctrl import TRANS_RPC_ADDRESS
from trans_client import TransClient

SpuLogging.info("\tRPC trans address:%s,\t port:%s" % (TRANS_RPC_ADDRESS[0], TRANS_RPC_ADDRESS[1]))

trans_client = TransClient()
trans_client.connect(TRANS_RPC_ADDRESS)
trans_client.setOperator("leo_api")

