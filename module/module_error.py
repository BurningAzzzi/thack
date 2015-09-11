#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © meishixing.com 
# Date  : 2013-07-03  
# Author: niusmallnan
# Email : <zhangzhibo521@gmail.com>
#
# Distributed under terms of the MIT license.

"""

"""

from sputnik.SpuError import SpuError, SpuErrorCodeGen

__code_gen = None

def code():
    global __code_gen
    if not __code_gen:
        # 100 -- 200
        __code_gen = SpuErrorCodeGen(100)
    return __code_gen.code()

class ModuleError(SpuError):
    code()



