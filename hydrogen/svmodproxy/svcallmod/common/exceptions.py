#encoding: utf-8
'''
Created on 2014��7��4��

@author: sony
'''
from hydrogen.common.exceptions import HydrogenException
class NoSvModException(HydrogenException):
	message='No Service with the id: %(sv_id)s' 
