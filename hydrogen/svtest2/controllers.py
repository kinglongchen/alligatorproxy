#!/bin/python
from hydrogen.v1.controllers import Controller
from hydrogen import policy
from hydrogen.common import exceptions
class Hello(Controller):
	def index(self,req):
		context= req.environ['hydrogen.context']
		target = {'tenant_id':'2f11cefc7b1940bfb41598c70ae3bdf2','test_name':456}
		action = 'get_test_action'
		policy.init()
		try:
			policy.enforce(context,action,target)
		except Exception,e:
			return e.msg
		return "Hello world!!!"
	def show(self,req,id):
		return "Hello World!!!"+str(id)
	def echo_hello(self,req):
		return "echo_hello():Hello world!!!"
