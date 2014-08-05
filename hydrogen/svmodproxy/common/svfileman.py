# encoding: utf-8
'''
Created on 2014年6月14日

@author: sony
'''
import os
from hydrogen.svmodproxy.common import exceptions
SERVICE_FILE_PATH='/var/service/'
svtypedic={'py':'python/','svc':'svc/'}
#svmidfiletype_dict={'python':['pyc']}
svsuf_map={'python':'py','svc':'svc'}


class SvFileMan(object):
	def __init__(self):
		self._svfilepath=SERVICE_FILE_PATH
			
# 	def findfile2(self,sv_id):
# 		svfilepath=''
# 		svsuf=''
# 		for root,dirs,files in os.walk(self._svfilepath):
# 			svtype=root.split('/')[-2]
# 			svmtps=svmidfiletype_dict.get(svtype,[])
# 			for file in files:
# 				if str(sv_id)==file.split('.')[0].strip() and file.split('.')[-1] not in svmtps:
# 					svfilepath=root+'/'+file
# 					svsuf=file.split('.')[-1].strip()
# 					break
# 			if svfilepath:
# 				break
# 		if not svfilepath:
# 			raise exceptions.NoServiceError(sv_id=sv_id)
# 		return svfilepath,svsuf
	
	
	
	
	def findfile(self,sv_id):
		svfilepaths=[]
		for root,dirs,files in os.walk(self._svfilepath):
			svtype=root.split('/')[-2]
			for file in files:
				if str(sv_id)==file.split('.')[0].strip():
					svfilepaths.append(root+'/'+file)
			if svfilepaths:
				break
		if not svfilepaths:
			raise exceptions.exceptions.NUllResourceIDException(id=sv_id)
		return svfilepaths
	
	
	def fileSave(self,filename,filedata):
		svsuf=filename.split('.')[-1].strip()
		if svsuf not in svtypedic.keys():
			svtype='other/'
		else:
			svtype=svtypedic[svsuf]
		svtypepath=self._svfilepath+svtype
		if not os.path.exists(svtypepath):
			os.makedirs(svtypepath)
		f=file(svtypepath+filename,'w')
		f.write(filedata)
		f.close()
		return True
	
		
	def fileDelete(self,filename):
		return os.remove(filename)
	
	def svFileFind(self,sv_id):
		svfile=''
		svsuf=''
		svfilepaths=self.findfile(sv_id)
		svfiledir=svfilepaths[0].split('/')[-2]
		svsuf=svsuf_map.get(svfiledir)
		for svfilepath in svfilepaths:
			suffix=svfilepath.split('.')[-1]
			if suffix==svsuf:
				svfile=svfilepath
				break
		return svfile,svsuf
		
		
		
		
	def svFileSave(self,svname,svdata):
		self.fileSave(svname,svdata)
	
	def svFileDelete(self,id):
		filenames=self.findfile(id)
		for filename in filenames:
			self.fileDelete(filename)