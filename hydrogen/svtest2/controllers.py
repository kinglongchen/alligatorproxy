#!/bin/python
from v1.controllers import Controller
class Hello(Controller):
	def index(self,req):
		print req.environ['neutron.context']
		return "Hello world!!!"
	def show(self,req,id):
		return "Hello World!!!"+str(id)
	def echo_hello(self,req):
		return "echo_hello():Hello world!!!"
