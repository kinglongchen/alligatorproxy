#encoding: utf-8
'''
Created on 2014年7月15日

@author: sony
'''
import xengin
import sys
import json
from hydrogen.common.exceptions import HydrogenException
from hydrogen.common import db
from hydrogen.svmodproxy.svcallmod.common import service
from hydrogen.common import logger

class SvcCall(service.Service):
	def call(self,svfilename,*args,**kwargs):
		#根据svfile获得相应服务组合描述性文件，并转换成json格式
		svcf=open(svfilename)
		svcj=json.loads(svcf.read())
		svcf.close()
		try:
			rs = xengin.exc(svcj, kwargs)
		except HydrogenException,e:
			return e.msg
		except Exception,e:
			logger.error(e.message)
			return e.message
		return rs
	
	def stop(self):
		pass