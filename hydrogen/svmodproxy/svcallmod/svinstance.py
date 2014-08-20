#encoding: utf-8
'''
Created on 2014年8月1日

@author: sony
'''
import threading
import Queue
from svcb import ServiceCtrlBlock
import svcall
import traceback
from hydrogen.svmodproxy.svcallmod.common import exceptions
from hydrogen.common.exceptions import NUllResourceIDException,HydrogenException
from hydrogen.common import logger as Logger



def lock_deco(fun):
	def new_fun(self,*args,**kwargs):
		self.method_lock.acquire()
		try:
			return fun(self,*args,**kwargs)
		finally:
			self.method_lock.release()
	return new_fun
		
class SvInstance(threading.Thread):
	def __init__(self,sv_inst_id,user_id,sv_id,svtype=ServiceCtrlBlock.UNDAEM):
		super(SvInstance,self).__init__()
		self.__conn_queue = Queue.Queue()
		self.builded=False
		self.method_lock = threading.Lock()
		#线程初始化
		self.__building(sv_inst_id, user_id, sv_id, svtype)
			
	@lock_deco
	def start(self):
# 		if self.svcb.is_asy() and self.svcb.is_ready():
		if self.svcb.is_error():
			raise exceptions.SVInstanceErrorException(error_msg=self.svcb.error_msg)
		if self.svcb.is_stop():
			raise exceptions.SVInstanceException(message='The Service Insetance Has been Stopped:%s' %self.svcb.id)
		if not self.svcb.is_builed():
			raise exceptions.SVInstanceStateException(cur_state=self.svcb.state,need_state=ServiceCtrlBlock.BUILDED)
		super(SvInstance,self).start()
	
	@lock_deco	
	def service_call(self,data):
# 		if not self.svcb.is_
		if self.svcb.is_error():
			raise exceptions.SVInstanceErrorException(error_msg=self.svcb.error_msg)
		if self.svcb.is_stop():
			raise exceptions.SVInstanceException(message='The Service Insetance Has been Stopped:%s' %self.svcb.id)
		if not self.svcb.is_ready() or self.svcb.is_suspend():
			raise exceptions.SVInstanceStateException(cur_state=self.svcb.state,need_state=ServiceCtrlBlock.READY) 
			'''
			向线程发送数据，让其处理，等待线程处理完数据，但这只有
			1.向线程发送需要处理的数据
			2.判断是否为后台程序
				(1).是：不等待处理的数据
				(2).否：等待线程返回处理的数据，如果在规定的时间内没有返回的数据，则抛出异常
			3.返回结果
			'''
		
		output_queue=Queue.Queue()
		self.__conn_queue.put((data,output_queue))
		if self.svcb.is_undaem():
			data = output_queue.get(True,4)
			return data
		
	@lock_deco	
	def suspend(self):
		if self.svcb.is_error():
			raise exceptions.SVInstanceErrorException(error_msg=self.svcb.error_msg)
		if self.svcb.is_stop():
			raise exceptions.SVInstanceException(message='The Service Insetance Has been Stopped:%s' %self.svcb.id)
		self.svcb.ready_to_suspend()
		
	@lock_deco	
	def resume(self):
		if self.svcb.is_error():
			raise exceptions.SVInstanceErrorException(error_msg=self.svcb.error_msg)
		if self.svcb.is_stop():
			raise exceptions.SVInstanceException(message='The Service Insetance Has been Stopped:%s' %self.svcb.id)
		if not self.svcb.is_suspend():return
		self.svcb.suspend_to_ready()
	
	@lock_deco	
	def close(self):
		if self.svcb.is_error():
			raise exceptions.SVInstanceErrorException(error_msg=self.svcb.error_msg)
		if self.svcb.is_stop():
			raise exceptions.SVInstanceException(message='The Service Insetance Has been Stopped:%s' %self.svcb.id)
		if self.svcb.is_ready() or self.svcb.is_running() or self.svcb.is_suspend():
			self.__conn_queue.put((None,None))
		self.__conn_queue.join()
		self.svcb.to_stop()
	
	def __building(self,sv_inst_id,user_id,sv_id,svtype=ServiceCtrlBlock.UNDAEM):
		self.svcb = ServiceCtrlBlock(sv_inst_id,user_id,sv_id,svtype)
		self.svcb.building_to_builded()
		self.builded=True
		self.svcb.thread=self
	
	def run(self):
		try:
			while(True):
				if (self.svcb.is_running()):
					self.svcb.running_to_ready()
				if (self.svcb.is_builed()):
					self.svcb.builded_to_ready()
				data,output_queue = self.__conn_queue.get()
				if data is None and output_queue is None:
					self.svcb.to_stop()
					self.__conn_queue.task_done()
					break
			
				self.svcb.ready_to_running()
			
				#一次服务运行服务运行
					#data = self.sv_call_mgr.svCall(self.svcb.sv_id, data)
				data = svcall.svCall(self.svcb.sv_id, data)
				output_queue.put(data)
				self.__conn_queue.task_done()
		except Exception,e:
			Logger.error(e.message)
			self.svcb.error_msg = e.message
		
		
			
class SvInstanceMgr(object):
	def __init__(self):
		self.__svinstant_dict={}
	
	def build_svinstance(self,sv_inst_id,user_id,sv_id,svtype=ServiceCtrlBlock.UNDAEM):
		if self.__svinstant_dict.has_key(sv_inst_id):
			raise exceptions.SVInstanceException(message='The Servcie Instance is Exist:%s' %sv_inst_id)
		self.__svinstant_dict[sv_inst_id]=SvInstance(sv_inst_id, user_id, sv_id, svtype)
	
	
	def start(self,sv_inst_id):
		
		self.getSvInstance(sv_inst_id).start()
	
	def getSvInstance(self,sv_inst_id):
		svinst = self.__svinstant_dict.get(sv_inst_id,None)
		if svinst is None:
			raise NUllResourceIDException(id=sv_inst_id)
		
		return svinst
	
	def suspend(self,sv_inst_id):
		self.getSvInstance(sv_inst_id).suspend()
		
	def resume(self,sv_inst_id):
		self.getSvInstance(sv_inst_id).resume()
		
	def close(self,sv_inst_id):
		self.getSvInstance(sv_inst_id).close()
		self.getSvInstance(sv_inst_id).join()
		del self.__svinstant_dict[sv_inst_id]
	
	def service_call(self,sv_inst_id,data):
		return self.getSvInstance(sv_inst_id).service_call(data)
	
	def get_svinst_state(self,sv_inst_id):
		return self.getSvInstance(sv_inst_id).svcb.state
	
	def get_svinst_error_msg(self,sv_inst_id):
		return self.getSvInstance(sv_inst_id).svcb.error_msg
		
	def close_all(self):
		for sv_inst_id in self.__svinstant_dict.keys():
			self.close(sv_inst_id)
			
	def get_all_state(self):
		rsdict = []
		for svinst in self.__svinstant_dict.itervalues():
			rsdict.append(svinst.svcb)
		return rsdict
	
	def print_svinstant_dict(self):
		print self.__svinstant_dict
	
	