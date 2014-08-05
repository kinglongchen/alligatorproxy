#!/bin/python
class Controller(object):
	def default(self,req,id=None):
		print "Start"
		print id
		print "End"
		return "Action Not Define!!!"
