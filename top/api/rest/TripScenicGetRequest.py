'''
Created by auto_sdk on 2015.09.06
'''
from top.api.base import RestApi
class TripScenicGetRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.scenic_id = None

	def getapiname(self):
		return 'taobao.trip.scenic.get'
