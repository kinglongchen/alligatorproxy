#!/bin/python
from v1 import wsgi
import controllers
class Public():
	def add_routes(self,mapper):
		controller = controllers.Tenant()
		mapper.connect('/tenants',  
                       controller=wsgi.Resource(controller),  
                       action='get_projects_for_token',  
                       conditions=dict(method=['GET'])) 
		mapper.resource('name','names',
						controller=wsgi.Resource(controllers.ListName()))
