#!/bin/python
#encoding: utf-8
from hydrogen.v1.controllers import Controller
from hydrogen import policy
from hydrogen.svmodproxy.common import exceptions
from common import svfileman
from svcallmod import svcall
import cgi
import os
from svcallmod import svinstance
from svcallmod.svcb import ServiceCtrlBlock

from webob import Request, Response 

svfileman=svfileman.SvFileMan()
class VMSVManProxy(Controller):
	def __init__(self):
		self.svinstanc_mgr = svinstance.SvInstanceMgr
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
		except exceptions.exceptions.NUllResourceIDException,e:
			res.status=404
		return res.status
	
	
	def svCall(self,req,id,sv_inst_id,body=None):
		#将通过请求体发送的json格式的数据和通过url发送的数据保存到字典中
		res =Response(None,200)
		kwargs=(dict(body) if body else dict())
		kwargs.update(req.GET.dict_of_lists())
		try:
			rs=self.svinstanc_mgr.service_call(sv_inst_id, kwargs)
			res.body=rs
		except exceptions.exceptions.NUllResourceIDException,e:
			res.status=404
		return rs
	
	def buildSvInst(self,req,id,body=None):
		#启动一个服务后，这个服务才能被调用
		#url Post http://ip:port/v1/sv_id/start
		#body:user_id,sv_inst_id,type
# 		if body['svtype']==utils.SYN:
		res =Response(None,200)
		sv_inst_id = body['sv_inst_id']
		sv_id = id
		user_id = body['user_id']
		svtype=body['svtype']
		if svtype not in ServiceCtrlBlock.TYPES:
			res.status=412
		self.svinstanc_mgr.build_svinstance(sv_inst_id, user_id, sv_id, svtype)
		return res
	
	def svStatequery(self,req,id,sv_inst_id,body=None):
		#GET http://ip:port/v1/sv_id/sv_inst_id
		res =Response(None,200)
		try:
			return self.svinstanc_mgr.get_svinst_state(sv_inst_id)
		except exceptions.exceptions.NUllResourceIDException,e:
			res.status=404
		return res
	
	def svSuspend(self,req,id,sv_inst_id):
		#UPDATE http://ip:port/v1/sv_id/sv_inst_id
		res =Response(None,200)
		try:
			self.svinstanc_mgr.suspend(sv_inst_id)
		except exceptions.exceptions.NUllResourceIDException,e:
			res.status=404
		return res
	
	def svClose(self,req,id,sv_inst_id):
		#DELETE http://ip:port/v1/sv_id/sv_inst_id
		res =Response(None,200)
		try:
			self.svinstanc_mgr.close(sv_inst_id)
		except exceptions.exceptions.NUllResourceIDException,e:
			res.status=404
		return res
	
	