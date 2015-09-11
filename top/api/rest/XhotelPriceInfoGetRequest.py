'''
Created by auto_sdk on 2015.09.06
'''
from top.api.base import RestApi
class XhotelPriceInfoGetRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.end_date = None
		self.pid = None
		self.shid_city_code = None
		self.start_date = None

	def getapiname(self):
		return 'taobao.xhotel.price.info.get'
