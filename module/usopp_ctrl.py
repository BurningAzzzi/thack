#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Date   : 2015-01-26
# Author : biluochun
# Email  : biluochun@lanrenzhoumo.com

from sputnik.SpuLogging import *
from module.base_ctrl import USOPP_RPC_ADDRESS
from usopp_client import UsoppClient

SpuLogging.info("\tRPC usopp address:%s,\t port:%s" % (USOPP_RPC_ADDRESS[0],
                                                       USOPP_RPC_ADDRESS[1]))

usopp_client = UsoppClient()
usopp_client.connect(USOPP_RPC_ADDRESS)
