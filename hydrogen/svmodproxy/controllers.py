#!/bin/python
#encoding: utf-8


#测试
# import sys
# import os
# sys.path.append('/root/alligatorproxy/')
# sys.path.append('/root/alligatorproxy/hydrogen')


from hydrogen.v1.controllers import Controller
from hydrogen import policy
from hydrogen.svmodproxy.common import exceptions
from hydrogen.common.exceptions import NUllResourceIDException
from common import svfileman
from svcallmod import svcall
import cgi
import os
from svcallmod import svinstance
from svcallmod.svcb import ServiceCtrlBlock
from hydrogen.common import logger as Logger
from webob import Request, Response 
import json

svfileman=svfileman.SvFileMan()
class VMSVManProxy(Controller):
	def __init__(self):
		self.svinstanc_mgr = svinstance.SvInstanceMgr()
	def fileDeploy(self,req):
		res =Response(None,200)
		environ = req.environ
		fileds=cgi.FieldStorage(environ["wsgi.input"],environ=environ)
		sv_file = fileds['svfile'].value
		sv_filename=fileds['svfile'].filename
		svfileman.svFileSave(sv_filename, sv_file)
		return res
	
	def fileUndeploy(self,req,id):
		res =Response(None,200)
		try:
			svfileman.svFileDelete(id)
		except NUllResourceIDException,e:
			res.status=404
		return res.status
	
	
	def svCall(self,req,id,sv_inst_id,body=None):
		#将通过请求体发送的json格式的数据和通过url发送的数据保存到字典中
		res =Response(None,200)
		kwargs=(dict(body) if body else dict())
		if req:
			kwargs.update(req.GET.dict_of_lists())
		try:
			rs=self.svinstanc_mgr.service_call(sv_inst_id, kwargs)
			rs = json.dumps(rs)
			res.body=rs
		except NUllResourceIDException,e:
			Logger.error(e.msg)
			res.status=404
		except Exception,e:
			Logger.error(e.message)
			res.status=505
		return res
	
	def buildSvInst(self,req,id,body=None):
		#启动一个服务后，这个服务才能被调用
		#url Post http://ip:port/v1/sv_id/start
		#body:user_id,sv_inst_id,type
# 		if body['svtype']==utils.SYN:
		res =Response(None,200)
# 		sv_inst_id = body['sv_inst_id']
		sv_inst_id = str(body.get('sv_inst_id'))
		if not sv_inst_id:
			Logger.debug("The args 'sv_inst_id' can not be null!")
			res.status=505
		sv_id = id
		
		user_id = body.get('user_id')
		if not user_id:
			Logger.debug("The args 'user_id' can not be null!")
			res.status=505
		svtype = body.get('svtype')
		if svtype is None:
			svtype = ServiceCtrlBlock.UNDAEM
		if svtype not in ServiceCtrlBlock.TYPES:
			res.status=412
		try:
			self.svinstanc_mgr.build_svinstance(sv_inst_id, user_id, sv_id, svtype)
			self.svinstanc_mgr.start(sv_inst_id)
		except Exception,e:
			Logger.error(e.msg)
			res.status=505
			res.body=e.msg
		return res
	
	def svStatequery(self,req,id,sv_inst_id,body=None):
		#GET http://ip:port/v1/sv_id/sv_inst_id
		res =Response(None,200)
		state_msg={}
		try:
			rs = self.svinstanc_mgr.get_svinst_state(sv_inst_id)
			state_msg['state']=rs
			if rs==ServiceCtrlBlock.ERROR:
				state_msg['error_msg']=self.svinstanc_mgr.get_svinst_error_msg(sv_inst_id)
			state_msg = json.dumps(state_msg)
			res.body = state_msg
		except NUllResourceIDException,e:
			Logger.error(e.message)
			res.status=404
		except Exception,e:
			Logger.error(e.message)
			res.status=505
# 			res.body=e.message
		return res
	
	def svSuspend(self,req,id,sv_inst_id,body=None):
		#UPDATE http://ip:port/v1/sv_id/sv_inst_id
		res =Response(None,200)
		try:
			self.svinstanc_mgr.suspend(sv_inst_id)
		except NUllResourceIDException,e:
			Logger.error(e.message)
			res.status=404
		except Exception,e:
			Logger.error(e.message)
			res.status=505
			res.body = e.message
		return res
	
	def svResume(self,req,id,sv_inst_id,body=None):
		res = Response(None,200)
		try:
			self.svinstanc_mgr.resume(sv_inst_id)
		except NUllResourceIDException,e:
			Logger.error(e.message)
			res.status=404
		except Exception,e:
			Logger.error(e.message)
			res.status=505
			res.body = e.message
		return res
		#使得服务实例的状体转换换为READY状态
		
	def svClose(self,req,id,sv_inst_id):
		#DELETE http://ip:port/v1/sv_id/sv_inst_id
		res =Response(None,200)
		try:
			self.svinstanc_mgr.close(sv_inst_id)
		except NUllResourceIDException,e:
			Logger.error(e.message)
			res.status=404
		except Exception,e:
			Logger.error(e.message)
			res.status=505
			res.body=e.message
		return res
	
	def closeAll(self,req):
		res =Response(None,200)
		try:
			self.svinstanc_mgr.close_all()
		except Exception,e:
			Logger.error(e.message)
			res.status=505
			res.body=e.messag
		return res


# import traceback
# vmsvproxy = VMSVManProxy()
# 
# 		
# vmsvproxy.buildSvInst(None, '93', {'sv_inst_id':'0','user_id':'0123'})
# #vmsvproxy.buildSvInst(None, '93', {'sv_inst_id':'1','user_id':'0123'})
# 
# try:
# 	while True:
# 		user_input_args_str = raw_input()
# 		user_input_args=user_input_args_str.split(' ')
# 		user_input = user_input_args[0]
# 		args =user_input_args[1:]
# 		
# 		if user_input=='quit':
# 			vmsvproxy.closeAll(None)
# 			break
# 			
# 		if user_input=='close':
# 			if not args:
# 				print 'args can not be Null'
# 			else:
# 				print vmsvproxy.svClose(None, None, args[0])
# 				
# 		if user_input=='help':
# 			print 'welcome!'
# 			
# 		if user_input=='all_state':
# 			print vmsvproxy.svinstanc_mgr.get_all_state()
# 			
# 		if user_input=='state':
# 			if not args:
# 				print 'args can not be Null'
# 			else:
# 				print vmsvproxy.svStatequery(None,None,args[0],None)
# 	
# 		if user_input=='call':
# 			if not args:
# 				print 'args can not be Null'
# 			else:
# 				print vmsvproxy.svCall(None,None,args[0],None)
# 		if user_input=='suspend':
# 			if not args:
# 				print 'args can not be Null'
# 			else:
# 				print vmsvproxy.svSuspend(None, None, args[0])
# 		
# 		if user_input=='resume':
# 			if not args:
# 				print 'args can not be Null'
# 			else:
# 				print vmsvproxy.svResume(None, None, args[0])
# 		
# except Exception,e:
# 	traceback.print_exc()
# 	vmsvproxy.closeAll(None)
# 	exit
# except 	KeyboardInterrupt:
# 	vmsvproxy.closeAll(None)
# 	exit
# except TypeError:
# 	print 'asdfasdf'
# 	vmsvproxy.closeAll(None)
# 	exit
	
	