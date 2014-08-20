#encoding: utf-8
'''
Created on 2014��7��4��

@author: sony
'''
from hydrogen.common import exceptions

class SvModProxyException(exceptions.HydrogenException):
	pass


class ServiceExecutorException(SvModProxyException):
	pass

class UnknownServiceExecutorException(ServiceExecutorException):
	message="Unkown Service suffix:%(suffix)s"
