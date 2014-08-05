#!/bin/python
from v1 import wsgi
import controllers
class Public():
	def add_routes(self,mapper):
		#mapper.resource('test','tests',controller=wsgi.Resource(controllers.Hello()))
		dbmgrctl=controllers.DBMgrCtl()
		mapper.connect('/createdb',controller=wsgi.Resource(dbmgrctl),action='createdb')
		mapper.connect('/deletedb',controller=wsgi.Resource(dbmgrctl),action='deletedb')
