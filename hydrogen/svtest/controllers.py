#!/bin/python
from v1.controllers import Controller
#class Controller(object):
#	def default(self,req,id):
#		print "Start"
#		print id
#		print "End"
##		return "Action Not Define!!!"
		
class Tenant(Controller):
    def __init__(self):
        print "ControllerTest!!!!"
    def get_projects_for_token(self,req):
          print "req",req
          return {
            'name': "test",
            'properties': "test"
        }
class TestDemo(Controller):
	def __init__(self):
		print "ListName!!!"
	def index(self,req):
		db_session=req.environ['db_session']
		
		return "list all resources"
	def show(self,req,id):
		print "START"
		print id
		print "END"
		return "Have id"+id
