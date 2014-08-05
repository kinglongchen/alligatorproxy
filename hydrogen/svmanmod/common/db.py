# encoding: utf-8
'''
Created on 2014��6��11��

@author: sony
'''
import vmmanmod_client
def getSvVmip(db_session,id):
	sql='selete vm_id from sv_tb where sv_id= '+id
	r=db_session.query(sql)
	vm_id=r[0][0]
	vm_ip=vmmanmod_client.get_vm_ip(vm_id)
	return vm_ip
def getSvsInfo4All(db_session):
	sql ='select * from sv_tb order by sv_id'
	return db_session.query(sql)

def getSvInfo4ID(db_session,id):
	sql = 'select sv_tb.sv_id as sv_id,sv_name,authority_type,sv_url,vm_id,user_id,sv_lang,sv_desc,sv_arg_id,arg_name,sv_arg_type_tb.arg_type_id as arg_type_id,arg_index,arg_direct,arg_type_name from sv_tb,sv_arg_type_tb,arg_type_tb where sv_tb.sv_id='+str(id)+' and sv_tb.sv_id=sv_arg_type_tb.sv_id and sv_arg_type_tb.arg_type_id = arg_type_tb.arg_type_id order by sv_id,arg_index;'
	print sql
	return db_session.query(sql)

def addSvInfo2TB(db_session,user_id,fileds):
	sv_name = fileds['sv_name'].value
	vm_id = fileds['vm_id'].value
	sv_lang=fileds['sv_lang'].value
	sv_desc=fileds['sv_desc'].value
	sql = 'insert into sv_tb(sv_name,vm_id,user_id,sv_lang,sv_desc) values ("'+sv_name+'","'+vm_id+'","'+user_id+'","'+sv_lang+'","'+sv_desc+'");'
	return db_session.insert(sql)


def addSvArgInfo2TB(db_session,sv_id,fileds,arg_direct=0):
	arg_name_key_prefix='input_arg_name'
	arg_names_key='input_arg_names'
	if arg_direct==1:
		arg_name_key_prefix = 'output_arg_name'
		arg_names_key = 'output_arg_names'
	arg_index = 0
	arg_names=fileds[arg_names_key].value.split(';')
	for arg_name in arg_names:
		arg_name_key=arg_name_key_prefix+str(arg_index)
		arg_type_id=fileds[arg_name_key].value
		sql = 'insert into sv_arg_type_tb(arg_name,sv_id,arg_type_id,arg_index,arg_direct) values ("'+arg_name+'","'+str(sv_id)+'","'+arg_type_id+'","'+str(arg_index)+'","'+str(arg_direct)+'");'
		print arg_name
		print arg_name_key
		print sql
		db_session.insert(sql)
		arg_index+=1
		
		
def addSvInputArg2TB(db_session,sv_id,fileds):
	addSvArgInfo2TB(db_session, sv_id, fileds, 0)
	
	
def addSvOutputArg2TB(db_session,sv_id, fileds):
	addSvArgInfo2TB(db_session, sv_id, fileds, 1)
	
	
def deleteInfoOnTB(db_session,id,tb):
	sql='delete from '+str(tb)+' where sv_id="'+str(id)+'"'
	print sql
	db_session.delete(sql)
	
def deleteSvInfoOnTB(db_session,sv_id):
	deleteInfoOnTB(db_session, sv_id,'sv_tb')
	
def deleteSvArg4IDOnTB(db_session,sv_id):
	deleteInfoOnTB(db_session, sv_id,'sv_arg_type_tb')
	
def updateSvOnTB(db_session,id,tb):
	pass
def updateSvArgtype(db_session,sv_arg_id,arg_type_info):
	arg_type_id=arg_type_info['arg_type_id']
	arg_name=arg_type_info['arg_name']
	if arg_type_id:
		sql = 'update sv_arg_type_tb set arg_type_id='+arg_type_id+' where sv_arg_id='+str(sv_arg_id)
		db_session.update(sql)
	if arg_name:
		sql = 'update sv_arg_type_tb set arg_name='+arg_name+' where sv_arg_id='+str(sv_arg_id)
		db_session.update(sql)

def updateSvTB(db_session,id,fileds):
	sql = 'update sv_tb set '
	for key in fileds.keys():
		sql+= str(key)+'='+str(fileds[key])+','
	#ɾ�����һ������
	sql=sql[:-1]
	sql+=' where sv_id='+str(id)
	db_session.update(sql)
def updatedSvUrl(db_session,id,sv_url):
	sql = 'update sv_tb set sv_url= "'+sv_url+'" where sv_id = "'+id+'"'
	db_session.update(sql)

		


	
	
	