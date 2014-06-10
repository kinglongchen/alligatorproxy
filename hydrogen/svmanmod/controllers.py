#!/bin/python
from v1.controllers import Controller
from common.vmmanmod_client import get_vm_ip
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
class ServiceMan(Controller):
	def __init__(self):
		print "ListName!!!"
	'''
	def get_html(self):
		html_f=open('html/upload.html','r')
		return html_f
	'''
	def index(self,req):
		user_id = req.environ['HTTP_X_USER_ID']
		user_name = req.environ['HTTP_X_USER_NAME'] 
		user_role = req.environ['HTTP_X_ROLES']
		db_session=environ['db_session']
		svs_json = {}
		svs_data = db_session.querySvs()

		input_args=[]
		input_arg={}
		output_args=[]
		output_arg={}
		svs = []
		sv={}
		sv_id = -1
		for sv_data in svs_data:
			if sv_id != sv_data['sv_id']:
				if sv_id != -1
					sv['input_arg_types']=input_args
					sv['output_arg_types']=output_args
					svs.append(sv)
					sv={}
				sv['sv_id']=sv_data['sv_id']
				sv['sv_name']=sv_data['sv_name']
				sv['authority_type']=sv_data['authority_type']
				sv['sv_url']=sv_data['sv_url']
				sv['vm_id']=sv_data['vm_id']
				sv['user_id']=sv_data['user_id']
				sv['sv_lang']=sv_data['sv_lang']
				sv['sv_desc']=sv_data['sv_desc']
				sv_id=sv_data['sv_id']
			if sv_data['arg_direct'] == 0:
				input_arg={}
				input_arg['arg_name'] = sv_data['arg__name']
				input_arg['arg_type_id'] = sv_data['arg_type_id']
				input_arg['arg_index'] = sv_data['arg_index']
				input_arg['arg_type_name'] = sv_data['arg_type_name']
			input_args.append(input_arg)
			if sv_data['arg_direct'] == 1:
				output_arg={}
				output_arg['arg_name'] = sv_data['arg__name']
				output_arg['arg_type_id'] = sv_data['arg_type_id']
				output_arg['arg_index'] = sv_data['arg_index']
				output_arg['arg_type_name'] = sv_data['arg_type_name']
			output_args.append(output_arg)
		svs_json['svs']=svs
		return svs
	def show(self,req,id):
		print "START"
		print id
		print "END"
		return "Have id"+id
	def create(self,req,body=None):
		environ = req.environ
		user_id = environ['HTTP_X_USER_ID']
		user_name = environ['HTTP_X_USER_NAME']
		user_role = environ['HTTP_X_ROLES']
		db_session=environ['db_session']
		# need to upgrade to use permission engine
		if user_role == 'nuser'
		return "you have no permission to upload service"
		try:
			request_body_size = int(environ.get('CONTENT_LENGTH',0))
		except ValueError:
			request_body_size=0
		fileds=cgi.FieldStorage(environ["wsgi.input"],environ=environ)
		sv_name = fileds['svname'].value
		vm_id = fileds['vm_id'].value
		sv_lang=fileds['sv_lng'].value
		sv_desc=fileds['sv_desc'].value
		#insert sv_tb table about service information
		sv_id=db_session.insertsvtb(sv_name,vm_id,user_id,sv_lang,sv_desc)	
		
		#update the sv_url about the service information		
		vm_ip = get_vm_ip(vm_id) #obtain vm ip addr
		sv_url = 'http://'+vm_ip+":8091/v1/svs/"+sv_id
		db_session.updatesv_url(sv_id,sv_url)
		#insert service arg information into sv_arg_type_tb table
		input_arg_name_arr=files['input_arg_names'].value.split(';')
		input_arg_index = 0
		for input_arg_name in input_arg_name_arr:
			f_arg_name="input_arg_name"+str(input_arg_index)
			arg_type_id=fileds[f_arg_name].value
			db_session.insertsvargtb(input_arg_name,str(sv_id),arg_type_id,input_arg_index,'0')
			input_arg_index+=1
			
		output_arg_name_arr=files['output_arg_names'].value.split(';')
		output_arg_index=0
		for output_arg_name in output_arg_name_arr
			f_arg_name="output_arg_name"+str(output_arg_index)
			arg_type_id=fileds[f_arg_name].value	
			db_session.insertsvargtb(output_arg_name,str(sv_id),arg_type_id,output_arg_index,'1')
			output_arg_index+=1

		sv_filename=sv_id+"."+fileds['svfile'].filename.split('.')[-1].strip()
		contenttype = envrion['CONTENT_TYPE']
		boundary=contenttype.split(';')[-1].split("=")[-1].strip()
		sv_data = self.multipartencode.encode(sv_filename,fileds['svfile'],boundary)
		#upload service to the vm
		return 'service upload successfully!!!'
