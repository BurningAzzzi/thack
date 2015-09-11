#! /usr/bin/env python
# -*- coding: utf-8 -*-

from config import cm
from leobase.tailor_ctrl import BizCustomCtrl, UserCustomCtrl,\
    BizUserContextCtrl, BizCustomImageCtrl, BizReadRidCtrl

biz_custom_ctrl = BizCustomCtrl(cm.TAILOR_DB_DATABASE)
user_custom_ctrl = UserCustomCtrl(cm.TAILOR_DB_DATABASE)
biz_custom_image = BizCustomImageCtrl(cm.TAILOR_DB_DATABASE)
biz_user_context_ctrl = BizUserContextCtrl(cm.TAILOR_DB_DATABASE)
biz_read_rid_ctrl = BizReadRidCtrl(cm.TAILOR_DB_DATABASE)
