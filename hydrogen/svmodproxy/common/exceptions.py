#encoding: utf-8
'''
Created on 2014��7��4��

@author: sony
'''
from hydrogen.common import exceptions

class SvModProxyException(exceptions.HydrogenException):
	pass

class NoServiceError(SvModProxyException):
	message = 'No Service named with the id:%(sv_id)s'
