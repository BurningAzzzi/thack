'''
Created by auto_sdk on 2015.09.06
'''
from top.api.base import RestApi
class XhotelListSearchRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.check_in = None
		self.check_out = None
		self.city_code = None
		self.city_name = None
		self.current_page = None
		self.dangcis = None
		self.dir = None
		self.high_price = None
		self.keywords = None
		self.low_price = None
		self.order = None
		self.page_size = None
		self.pid = None
		self.radius = None
		self.radius_lat = None
		self.radius_lng = None

	def getapiname(self):
		return 'taobao.xhotel.list.search'
