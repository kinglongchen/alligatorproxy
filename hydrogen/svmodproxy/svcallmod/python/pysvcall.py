#encoding: utf-8
'''
Created on 2014��6��30��

@author: sony
'''
from hydrogen.svmodproxy.svcallmod.common import exceptions
import sys
from hydrogen.svmodproxy.svcallmod.common import service


# class SvModMan(object):
# 	def __init__(self):
# 		self.modlist={}
# 		sys.path.append('/var/service/python')
# 	def importmod(self,modname):
# 		if modname in self.modlist.keys():
# 			self.modlist[modname]+=1
# 		else:
# 			self.modlist['modname']=0
# 		try:
# 			svmod=__import__(modname)
# 		except ImportError:
# 			raise exceptions.NoSvModException(sv_id=modname)
# 		return svmod
# 	
# 	def deletemod(self,modname):
# 		if modname in self.modlist.keys():
# 			if modname in sys.modules:
# 				del(sys.modules[modname])
# 			self.modlist.pop(modname)
# 	#服务调用模块的调度算法
# 	def modmandemo(self):
# 		pass
# 	
# svmodman=SvModMan()	
class PythonSv(service.Service):
	def __init__(self):
		self.modlist={}
		sys.path.append('/var/service/python')
		
	def __importmod(self,modname):
		if modname in self.modlist.keys():
			self.modlist[modname]+=1
		else:
			self.modlist['modname']=0
		try:
			svmod=__import__(modname)
		except ImportError:
				raise exceptions.NoSvModException(sv_id=modname)
		return svmod
	
	def __deletemod(self,modname):
		if modname in self.modlist.keys():
			if modname in sys.modules:
				del(sys.modules[modname])
			self.modlist.pop(modname)
	#服务调用模块的调度算法
	
	def __modmandemo(self):
		pass
	
	def call(self,svfilename,*args,**kwargs):
		try:
			svfilemod=svfilename.split('/')[-1].strip().split('.')[0].strip()
		except exceptions.HydrogenException,e:
			return e.msg
		sv=self.__importmod(svfilemod)
		return sv.main(*args,**kwargs)
	
# 
# def call(svfilename,*args,**kwargs):
# 	svfilemod=svfilename.split('/')[-1].strip().split('.')[0].strip()
# 	try:
# 		sv=svmodman.importmod(svfilemod)
# 	except exceptions.HydrogenException,e:
# 		return e.msg
# 	return sv.main(*args,**kwargs)



