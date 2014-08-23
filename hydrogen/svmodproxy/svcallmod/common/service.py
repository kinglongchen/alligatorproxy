#encoding: utf-8
'''
Created on 2014年8月4日

@author: sony
'''
from abc import ABCMeta,abstractmethod,abstractproperty
class Service(object):
	__metaclass__ = ABCMeta
	@abstractmethod
	def call(self,**kwargs):
		pass
# 	@abstractmethod
# 	def stop(self):
# 		pass
