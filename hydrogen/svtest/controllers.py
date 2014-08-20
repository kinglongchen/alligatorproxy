#!/bin/python
from hydrogen.v1.controllers import Controller
import time
#class Controller(object):
#	def default(self,req,id):
#		print "Start"
#		print id
#		print "End"
##		return "Action Not Define!!!"
tid=id
tv=0
class Tenant(Controller):
    def __init__(self):
    	pass
    def get_projects_for_token(self,req):
          print "req",req
          return {
            'name': "test",
            'properties': "test"
        }
class TestDemo(Controller):
	def __init__(self):
		self.tv=0
	def index(self,req):
# 		global self.tv
		print self.tv
		print tid(self.tv)
		time.sleep(10)
		self.tv+=1
		return 'index'
	def show(self,req,id):
# 		global tv
		print self.tv
		print tid(self.tv)
		return 'show'

# td = TestDemo()
# td.index(None)
# td.show(None,None)