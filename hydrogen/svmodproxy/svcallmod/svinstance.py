#encoding: utf-8
'''
Created on 2014年8月1日

@author: sony
'''
import threading
import Queue
from svcb import ServiceCtrlBlock
import svcall
from hydrogen.common import exceptions

class SvInstance(threading.Thread):
	def __init__(self,sv_inst_id,user_id,sv_id,svtype=ServiceCtrlBlock.UNDAEM):
		super(SvInstance,self).__init__()
		self.__conn_queue = Queue.Queue()
		self.builded=False
		#线程初始化
		self.building(sv_inst_id, user_id, sv_id, svtype)
			
	
	def start(self):
# 		if self.svcb.is_asy() and self.svcb.is_ready():
		if not self.svcb.is_builed():
			if self.svcb.is_error():
				raise Exception('Error:%s' %self.svcb.error_msg)
			else:
				raise Exception('The service instance is not in the builded state')
		super(SvInstance,self).start()
	
		
	def service_call(self,data):
# 		if not self.svcb.is_
		if self.svcb.is_ready():
			raise Exception('The service instance is not in the ready state') 
			'''
			向线程发送数据，让其处理，等待线程处理完数据，但这只有
			1.向线程发送需要处理的数据
			2.判断是否为后台程序
				(1).是：不等待处理的数据
				(2).否：等待线程返回处理的数据，如果在规定的时间内没有返回的数据，则抛出异常
			3.返回结果
			'''
		#判断服务是否在暂停状态
		if self.svcb.is_suspend():pass
		
		output_queue=Queue.Queue()
		self.__conn_queue.put((data,output_queue))
		if self.svcb.is_undaem():
			try:
				data = output_queue.get(True,4)
			except Queue.Empty,e:
				raise Exception('Timeout')
				
			return data
		
	def suspend(self):
		self.svcb.to_suspend()
	
	def close(self):
		self.__conn_queue.put((None,None))
		self.__conn_queue.join()
		
	def building(self,sv_inst_id,user_id,sv_id,svtype=ServiceCtrlBlock.UNDAEM):
		if self.builded:raise Exception('Have Builded Exception')
		self.svcb = ServiceCtrlBlock(sv_inst_id,user_id,sv_id,svtype)
		self.svcb.thread=self
		self.svcb.building_to_builded()
		self.builded=True
	
	def run(self):
		
		while(True):
			if (self.svcb.is_running()):
				self.svcb.running_to_ready()
			if (self.svcb.is_builed()):
				self.svcb.builded_to_ready()
			data,output_queue = self.__conn_queue.get()
			if data is None and output_queue is None:
				break
			self.svcb.ready_to_running()
			try:
			#一次服务运行服务运行
				#data = self.sv_call_mgr.svCall(self.svcb.sv_id, data)
				data = svcall.svCall(self.svcb.sv_id, data)
			except Exception,e:
				self.svcb.error_msg = e.message
			output_queue.put(data)

class SvInstanceMgr(object):
	def __init__(self):
		self.__svinstant_dict={}
	
	def build_svinstance(self,sv_inst_id,user_id,sv_id,svtype=ServiceCtrlBlock.UNDAEM):
		self.__svinstant_dict['sv_inst_id']=SvInstance(sv_inst_id, user_id, sv_id, svtype)
	
	
	def start(self,sv_inst_id):
		
		self.getSvInstance(sv_inst_id).start()
	
	def getSvInstance(self,sv_inst_id):
		svinst = self.__svinstant_dict.get(sv_inst_id,None)
		if svinst is None:
			raise exceptions.NUllResourceIDException(id=sv_inst_id)
		
		return svinst
	
	def suspend(self,sv_inst_id):
		self.getSvInstance(sv_inst_id).suspend()
	
	def close(self,sv_inst_id):
		self.getSvInstance(sv_inst_id).close()
		del self.__svinstant_dict[sv_inst_id]
	
	def service_call(self,sv_inst_id,data):
		return self.getSvInstance(sv_inst_id).service_call(data)
	
	def get_svinst_state(self,sv_inst_id):
		return self.getSvInstance(sv_inst_id).svcb.state
	
	