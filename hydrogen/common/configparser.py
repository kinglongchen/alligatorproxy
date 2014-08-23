#encoding: utf-8
'''
Created on 2014年8月8日

@author: sony
'''
import ConfigParser
CONFIG_PATH = 'config/hydrogen.conf'

class HydrogenConfigParser(ConfigParser.ConfigParser):
	def __init__(self,*args,**kwargs):
		ConfigParser.ConfigParser.__init__(self,*args,**kwargs)
		self.read(CONFIG_PATH)
		print CONFIG_PATH
		self.test_cfg = TestConfigparser()
	def vm_slaver_port(self):
		return self.get('VMSLAVER', 'port')
	
	def getTestSection(self,option,*args,**kwargs):
		return self.get('TEST', option,*args,**kwargs)
	
	def is_test(self):
		try:
			val = self.get('TEST','test')
		except ConfigParser.NoOptionError:
			val = 'False'
		if val.lower()=='true':
			return True
		elif val.lower()=='false':
			return False
		else:
			raise Exception("The value of option 'test' must be 'true' or 'false',and ignore case")
	
	def is_debug(self):
		try:
			val=self.get('DEFAULT', 'debug')
		except ConfigParser.NoOptionError:
			val = 'False'
		
		if val.lower()=='true':
			return True
		elif val.lower()=='false':
			return False
		else:
			raise Exception("The value of option 'debug' in the 'DEFUALT' section must be 'true' or 'false',and ignore case")
		
	def get_DB_config(self):
		db_config={}
		db_config['host'] = self.get('DATABASE','host')
		db_config['user'] = self.get('DATABASE','user')
		db_config['passwd'] = self.get('DATABASE','passwd')
		db_config['db'] = self.get('DATABASE','db')
		db_config['charset'] = self.get('DATABASE','charset')
		return db_config
	
	def get_DB_host(self):
		return self.get('DATABASE','host')
	
	def get_DB_user(self):
		return self.get('DATABASE','user')
	
	def get_DB_passwd(self):
		return self.get('DATABASE','passwd')
	
	def get_DB_db(self):
		return self.get('DATABASE','db')
	
	def get_DB_charset(self):
		return self.get('DATABASE','charset')

TEST_CONFIG_PATH = 'config/test.conf'
class TestConfigparser(ConfigParser.ConfigParser):
	def __init__(self,*args,**kwargs):
		ConfigParser.ConfigParser.__init__(self,*args,**kwargs)
		self.read(TEST_CONFIG_PATH)
cfg = HydrogenConfigParser()
# print configparser.is_test()
# print configparser.get('VMSLAVER', 'timeout')
# print configparser.get('DEFAULT', 'debug')
# print cfg.test_cfg.get('SERVER', 'vm_id')
# print cfg.test_cfg.get('SERVER', 'user_id')
# print cfg.test_cfg.get('SERVER', 'duration')
# print cfg.test_cfg.get('SERVER', 'create_time')
# print cfg.test_cfg.get('SERVER', 'user_role')
# print cfg.test_cfg.get('SERVER', 'vm_type')
# print cfg.test_cfg.get('SERVER', 'vm_name')
# print cfg.test_cfg.get('SERVER', 'vm_status')
# print cfg.test_cfg.get('SERVER', 'user_name')
# print cfg.test_cfg.get('SERVER', 'image_id')
# print cfg.test_cfg.get('SERVER', 'flavor_id')

