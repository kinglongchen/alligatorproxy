#encoding: utf-8
'''
Created on 2014��6��30��

@author: sony
'''
import sys
from python import pysvcall
from svxengin import svccall
import os
from hydrogen.svmodproxy.common import exceptions
from hydrogen.svmodproxy.common.svfileman import SvFileMan
from hydrogen.svmodproxy.svcallmod import svcb

#from hydrogen.svmodproxy.svcallmod import python
svexcmod_dic={'py':pysvcall.PythonSv(),'svc':svccall.SvcCall()}
svfileman=SvFileMan()
def svCall(sv_id,kwargs):
	#根据sv_id找到服务坐在目录以及服务的后缀svsuffix
	svfilename,svsuf=svfileman.svFileFind(sv_id)
	#根据svsuffix调用相应的服务调用模块
	svcall=svexcmod_dic.get(svsuf)
	if not svcall:
		raise exceptions.UnknownServiceExecutorException(suffix = svsuf)
	rs = svcall.call(svfilename,kwargs)
		#处理服务执行的错误情况
	return rs
	
		
	



