#encoding: utf-8
'''
Created on 2014��7��4��

@author: sony
'''
from hydrogen.svmodproxy.common.exceptions import SvModProxyException


class PythonServiceExcuteException(Exception):
	message='%(message)s'
			
class NoSvModException(SvModProxyException):
	message='No Service with the id: %(sv_id)s'
	
class SvCallException(SvModProxyException):
	message='%(message)s'
	

class SVInstanceException(SvCallException):
	message='%(message)s'
		
class SVInstanceStateException(SVInstanceException):
	message = 'Your action is not supported by the current state of the service:%(cur_state)s(need %(need_state)s)'
	
class SVInstanceErrorException(SVInstanceException):
	message = 'The Servcie is in the Error State:%(error_msg)s'

class SVCBException(SvCallException):
	message='%(message)s'

