'''
Created by auto_sdk on 2015.09.06
'''
from top.api.base import RestApi
class AlibabaTopOpenIpsectionGetRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)

	def getapiname(self):
		return 'alibaba.top.open.ipsection.get'
