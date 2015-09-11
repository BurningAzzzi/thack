'''
Created by auto_sdk on 2015.09.06
'''
from top.api.base import RestApi
class XhotelIncrementInfoGetRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.change_type = None
		self.current_page = None
		self.gmt_modified = None
		self.page_size = None

	def getapiname(self):
		return 'taobao.xhotel.increment.info.get'
