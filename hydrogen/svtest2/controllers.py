#!/bin/python
from v1.controllers import Controller
import policy
from common import exceptions
class Hello(Controller):
	def index(self,req):
		context= req.environ['neutron.context']
		target = {'test_id':123,'test_name':456}
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
