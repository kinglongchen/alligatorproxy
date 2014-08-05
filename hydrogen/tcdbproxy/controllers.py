#encoding: utf-8
#!/bin/python
from v1.controllers import Controller
import policy
from hydrogen.tcdbproxy.common import mysqldbmgr
class DBMgrCtl(Controller):
	def __init__(self):
		self.sqlmgr = mysqldbmgr.MysqlDBMgr()
	def createdb(self,req,body=None):
		dbname = body.get('dbname',None)
		db_username = body.get('db_username',None)
		db_passwd = body.get('db_passwd',None)
		#创建数据库名为dbname的数据库
		#创建用户名db_username；密码为db_passwd
		#赋予新创建的用户db_username只对dbname拥有权限
		rs = self.sqlmgr.createdb4user(db_username, db_passwd, dbname)
		return rs
	def deletedb(self,req,body=None):
		dbname=body.get('dbname',None)
		db_username = body.get('db_username',None)
		rs = self.sqlmgr.deletedb4user(dbname)
		return rs
