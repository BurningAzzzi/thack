#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
# Date  : 2015-09-11
# Author: Master Yumi
# Email : yumi@meishixing.com

from datetime import datetime
import math

def to_utf8(text):
    if isinstance(text, unicode):
        return text.encode("utf8")
    elif isinstance(text, datetime):
        return text.strftime("%Y-%m-%d %H:%M:%S")
    else:
        return str(text)

def calculate_distance(point1, point2):
    """计算距离"""
    return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2) * 100

