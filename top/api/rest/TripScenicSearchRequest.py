'''
Created by auto_sdk on 2015.09.06
'''
from top.api.base import RestApi
class TripScenicSearchRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.current_page = None
		self.distance = None
		self.keywords = None
		self.need_eticket = None
		self.need_today_booking = None
		self.p_id = None
		self.page_size = None
		self.scenic_types = None
		self.sort_field = None
		self.sort_order = None
		self.source_point = None

	def getapiname(self):
		return 'taobao.trip.scenic.search'
