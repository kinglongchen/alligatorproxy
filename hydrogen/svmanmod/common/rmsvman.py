'''
Created on 2014年6月11日

@author: sony
'''
import urllib2
import db
import vmmanmod_client
from MultiPartEncode import MultiPartEncode
class RmSVManClass(object):
	def __init__(self,db_session):
		self.db_session=db_session
		self.multipartencode=MultiPartEncode()
		
	def upload_file(self,vm_ip,contenttype,data):
		r = urllib2.Request("http://"+vm_ip+":8089/fileupload.app")
		r.add_unredirected_header('Content-Type',contenttype)
		r.add_data(data)
		u = urllib2.urlopen(r)
		return u

	def delete_file(self,vm_ip):
		'''
		req_url=""#websever调用url
		r.urllib2.Request(req_url)
		u=urllib2.urlopen(r)
		return u
		'''
		pass
	def addSv2Vm(self,vm_id,sv_id,sv_file,contenttype):
		vm_ip=vmmanmod_client.get_vm_ip(vm_id)
		sv_url = 'http://'+vm_ip+":8091/v1/svs/"+sv_id
		
		sv_filename=sv_id+"."+sv_file.filename.split('.')[-1].strip()
		boundary=contenttype.split(';')[-1].split("=")[-1].strip()
		sv_data = self.multipartencode.encode(sv_filename,sv_file,boundary)
		
		self.upload_file(vm_ip, contenttype, sv_data)
		return sv_url
		
	def deleteSvOnVM(self,id):
		#1.根据id获得服务所在vm
		#2.调用远程代理--一个webServer--删除远程vm上的服务程序
		sv_vmip=db.getSvVmip(self.db_session, id)
		self.delete_file(sv_vmip)
		