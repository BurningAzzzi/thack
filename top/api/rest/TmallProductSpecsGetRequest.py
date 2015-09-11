'''
Created by auto_sdk on 2015.09.06
'''
from top.api.base import RestApi
class TmallProductSpecsGetRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.cat_id = None
		self.product_id = None
		self.properties = None

	def getapiname(self):
		return 'tmall.product.specs.get'
