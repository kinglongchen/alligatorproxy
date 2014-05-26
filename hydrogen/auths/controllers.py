#/bin/python
from v1.controllers import Controller
from os import environ as env
import keystoneclient.v2_0.client as ksclient
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
		self.keystone=ksclient.Client(auth_url="http://controller:35357/v2.0",username="admin",password="ADMIN_PASS",tenant_name="admin")
		self.users=self.keystone.users
		self.roles=self.keystone.roles
		print "keystoneclient initialization successfully!"
	def index(self,req):
		return "auths test OK!!!"
	def show(self,req,id):
		print "START"
		print id
		print "END"
		return "Have id"+id
	def create(self,req,body=None):
		print "###########req.body"
		#print body
		print "###########req.POST"
		print req.POST['user']
		print "end"
		#username="demouser2"
		#userpasswd="12345"
		#useremail="demouser2@qq.com"
		#demo role id:
		#role_id="37b1edf63d6349eba5bbeb2c43cc6b66"
		#demo tenant id:
		#tenant_id="2f11cefc7b1940bfb41598c70ae3bdf2"
		#user=self.users.create(username,userpasswd,useremail)
		#print resp
		#self.roles.add_user_role(user,role_id,tenant_id)
		return "create user successfully!!!"
