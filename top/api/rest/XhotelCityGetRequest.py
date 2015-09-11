'''
Created by auto_sdk on 2015.09.06
'''
from top.api.base import RestApi
class XhotelCityGetRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.count = None
		self.start = None

	def getapiname(self):
		return 'taobao.xhotel.city.get'
