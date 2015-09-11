'''
Created by auto_sdk on 2015.09.06
'''
from top.api.base import RestApi
class XhotelInfoListGetRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.city_code = None
		self.current_page = None
		self.page_size = None
		self.pid = None
		self.shid = None

	def getapiname(self):
		return 'taobao.xhotel.info.list.get'
