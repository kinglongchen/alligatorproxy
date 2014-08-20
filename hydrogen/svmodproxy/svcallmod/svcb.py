#encoding: utf-8
'''
Created on 2014年8月1日

@author: sony
'''

import threading
import weakref
from hydrogen.svmodproxy.svcallmod.common import exceptions
	
class ServiceCtrlBlock(dict):
	'''
	SVCB类初始化时，主要设置服务实例下列属性：
	1.USER_ID该服务实例的服务ID
	2.SV_ID创建该服务的实例
	3.TYPE为服务的类型，一共有两个：守护(DAEM)和非守护(UNDAEM)
	4.STATE为服务的状态，分别有BUILDING,BUILDED,READY,RUNNING,SUSPEND,ERROR，当为ERROR时，ERROR_MSG有错误的信息
		提供了一个借口：state(svstate)来设置服务的状态
	5.ERROR_MSG为当服务为出现错误时，在这里有服务的信息
		提供了一个接口：error(error_msg)来设置服务错误，当设置为错误时，服务的状态则为ERROR
	6.SVTHREAD为当服务为异步(ASY)，这里存储服务的线程对象
	
	'''
	ID='ID'
	USER_ID='USER_ID'
	SV_ID='SV_ID'
	TYPE='TYPE'
	STATE='STATE'
	ERROR_MSG='ERROR_MSG'
	SVTHREAD='SVTHREAD'
	
	BUILDING,BUILDED,READY,RUNNING,STOP,SUSPEND,ERROR=('BUILDING','BUILDED','READY','RUNNING','STOP','SUSPEND','ERROR')
	DAEM,UNDAEM=('DAEM','UNDAEM')
	STATES=[BUILDING,BUILDED,READY,RUNNING,STOP,SUSPEND,ERROR]
	TYPES=[DAEM,UNDAEM]
	def __init__(self,id,user_id,sv_id,svtype=UNDAEM,svstate=BUILDING,error_msg=None,thread=None):
		super(ServiceCtrlBlock,self).__init__()
		self.__set_ID(id)
		self.__set_UserID(user_id)
		self.__set_SvID(sv_id)

		self.__set_Type(svtype)
		self.__set_State(svstate)
		
		self.__set_ErrorMsg(error_msg)
		
		self.__set_Thread(thread)
	@property
	def id(self):
		return self.get(self.ID)
	
	@property
	def sv_id(self):
		return self.get(self.SV_ID)
	
	@property
	def user_id(self):
		return self.get(self.USER_ID)
	
	@property
	def type(self):
		return self.get(self.TYPE)
	
	@property
	def state(self):
		return self.get(self.STATE)	
	
# 	@state.setter
# 	def state(self,svstates):
# 		self.__set_State(svstates)
	
	@property
	def error_msg(self):
		return self.get(self.ERROR_MSG)
	
	@error_msg.setter	
	def error_msg(self,error_msg):
		self.__set_ErrorMsg(error_msg)
		
	@property
	def thread(self):
		return self.get(self.SVTHREAD)
	
	@thread.setter
	def thread(self,svthread):
		if self.get(self.SVTHREAD):
			raise exceptions.SVCBException(message='The current thread object has been assigned:sv_inst_id=%s' %self.id)
		self.__set_Thread(svthread)
	
	def next_state(self):
		state = self.get(self.STATE)
		index = self.STATES.index(state)
		if index<3 and index>=0:
			self[self.STATE] = self.STATES[index+1]
	
	def pre_state(self):
		state = self.get(self.STATE)
		index = self.STATES.index(state)
		if index<=3 and index>0:
			self[self.STATE] = self.STATES[index-1]
			
	def building_to_builded(self):
		if not self.is_building():
			raise exceptions.SVCBException(message='The current state is not in building')
		self.next_state()
# 		self[self.STATE]=self.BUILDED
	
	def builded_to_ready(self):
		if not self.is_builed():
			raise exceptions.SVCBException(message='The current state is not in builded')
		self.next_state()
# 		self[self.STATE]=self.READY

	def ready_to_running(self):
		if not self.is_ready():
			raise exceptions.SVCBException(message='The current state is not in ready')
		self.next_state()
# 		self[self.STATE]=self.RUNNING
	
	def running_to_ready(self):
		if not self.is_running():
			raise exceptions.SVCBException(message='The current state is not in running')
		self.pre_state()
# 		self[self.STATE]=self.READY
	def ready_to_suspend(self):
		if not self.is_ready():
			raise exceptions.SVCBException(message='The current state is not in ready')
		self[self.STATE]=self.SUSPEND
	
	def suspend_to_ready(self):
		if not self.is_suspend():
			raise exceptions.SVCBException(message='The current state is not in suspend')
		self[self.STATE]=self.READY
		
	def to_error(self,error_msg):
		self.error_msg=error_msg
	
	#服务的暂停还需要自己考虑###############################################################################
	def to_suspend(self):
		self[self.STATE]=self.SUSPEND
	
	def to_stop(self):
		self[self.STATE]=self.STOP
	
	def running(self):
		self[self.STATE]=self.RUNNING
	
	def is_daem(self):
		'''
		判断是否是异步
		'''
		return self.get(self.TYPE)==self.DAEM
	
	def is_undaem(self):
		'''
		判断是否是同步
		'''
		return self.get(self.TYPE)==self.UNDAEM
	
	def is_ready(self):
		'''
		判断是否是就绪状态
		'''
		return self.get(self.STATE)==self.READY
	
	def is_building(self):
		'''
		判断是否是正在建立状态
		'''
		return self.get(self.STATE)==self.BUILDING
	
	def is_builed(self):
		'''
		判断是否已经创建成功
		'''
		return self.get(self.STATE)==self.BUILDED
	
	def is_running(self):
		'''
		判断是否是运行状态
		'''
		return self.get(self.STATE)==self.RUNNING
	
	def is_suspend(self):
		'''
		判断是否被挂起
		'''
		return self.get(self.STATE)==self.SUSPEND
	
	def is_error(self):
		'''
		判断是否错误
		'''
		return self.get(self.STATE)==self.ERROR
	
	def is_stop(self):
		'''
		判断是否关闭
		'''
		return self.get(self.STATE)==self.STOP
	
	def __set_ID(self,id):
		if not isinstance(id, str):
			raise exceptions.SVInstanceException(message='ErrorIDTYPE:%s,id=%s' %(type(id),id))
		self[self.ID]=str(id)
		
	
	def __set_UserID(self,user_id):
		if not (isinstance(user_id, str) or isinstance(user_id,unicode)):
			raise exceptions.SVInstanceException(message='ErrorUser_IDTYPE:%s,user_id=%s' %(type(user_id),user_id))
		self[self.USER_ID]=str(user_id)
		
	
	def __set_SvID(self,sv_id):
		if not (isinstance(sv_id, str) or isinstance(sv_id,unicode)):
			raise exceptions.SVInstanceException(message='ErrorSV_IDTYPE:%s,user_id=%s' %(type(sv_id),sv_id))
		self[self.SV_ID]=str(sv_id)
		
	def __set_State(self,svstate):
		'''
		设置SVCB的状态，如果状态值不在STATES中，则抛出异常
		如果状态不为ERROR，那么要清空ERROR_MSG
		'''
		if svstate not in self.STATES:
			raise exceptions.SVInstanceException(message='Unkown Service Instance State:%s' %svstate)
		self[self.STATE]=svstate
		
		if svstate != self.ERROR:
			self[self.ERROR_MSG]=None
		else:
			self[self.ERROR_MSG]='Unknown Error'
	
	def __set_Type(self,svtype):
		'''
		设置服务的类型，如果服务的类型不在规定的类型里面，抛出异常
		'''
		svtype=str(svtype)
		if svtype not in self.TYPES:
			raise exceptions.SVInstanceException(message='Unkown Service Instance Type:%s' %svtype)
		self[self.TYPE]=svtype
		
	
	def __set_ErrorMsg(self,error_msg):
		'''
		如果error_msg不为空，则设置staus为ERROR
		'''
		if not isinstance(error_msg, str):return
		self[self.STATE]=self.ERROR
		self[self.ERROR_MSG]=error_msg
		
	def __set_Thread(self,svthr):
		'''
		如果svthr为不为空，设置type为异步类型
		'''
		if svthr is None:return
		if not isinstance(svthr, threading.Thread):
			raise exceptions.SVInstanceException(message='ErrorThreadType:%s' %type(svthr))
		self[self.SVTHREAD]=weakref.ref(svthr)
	

	
#测试类
# t = ServiceCtrlBlock(id='1',user_id='12',sv_id='34')
# print t
# print t
# print 'state:'+t.state
# t.next_state()
# print 'state:'+t.state
# t.next_state()
# print 'state:'+t.state
# t.next_state()
# print 'state:'+t.state
# t.next_state()
# print 'state:'+t.state
# 
# print '#################'
# t.pre_state()
# print 'state:'+t.state
# t.pre_state()
# print 'state:'+t.state
# t.pre_state()
# print 'state:'+t.state
# t.pre_state()
# print 'state:'+t.state

# print 'id:'+t.id
# print 'user_id:'+t.user_id
# print 'sv_id:'+t.sv_id
# print 'type:'+str(t.type)
# t.error='test_error'
# t.state=READY
# print 'state:'+str(t.state)
# print 'error_msg:'+str(t.error)
# print 'svthread:'+str(t.svthr)

# class ServiceCtrlBlockMgr(object):
# 	
# 	def __init__(self):
# 		self.svcbs={}
# 		
# 	def initsvcb(self,sv_inst_id,user_id,sv_id,svtype=SYN):
# 		svcb = ServiceCtrlBlock(sv_inst_id,user_id,sv_id,svtype)
# 		self.svcbs[sv_inst_id]=svcb
# 		return svcb
# 	def addsvcb(self,sv_inst_id,user_id,sv_id):
# 		svcb = ServiceCtrlBlock(sv_inst_id,user_id,sv_id)
# 		self.svcbs[sv_inst_id]=svcb
# 		return svcb
# 		
# 
# 	def getsvcb(self,sv_inst_id):
# 		return self.svcbs.get(sv_inst_id,None)

#测试
# svcb_mgr=ServiceCtrlBlockMgr()
# svcb_mgr.addsvcb(sv_inst_id='1',user_id='12',sv_id='34')
# svcb = svcb_mgr.getsvcb('1')
# print svcb.state
# svcb.state=READY
# 
# svcb2 = svcb_mgr.getsvcb('1')
# print svcb2.state
		