'''
Created by auto_sdk on 2015.09.06
'''
from top.api.base import RestApi
class TripTravelSearchRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.current_page = None
		self.dest_city = None
		self.from_city = None
		self.keyword = None
		self.max_price = None
		self.min_price = None
		self.p_id = None
		self.page_size = None
		self.travel_category = None
		self.travel_days = None
		self.travel_months = None

	def getapiname(self):
		return 'taobao.trip.travel.search'
