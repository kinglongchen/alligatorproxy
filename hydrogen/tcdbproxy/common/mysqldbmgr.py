#encoding: utf-8
'''
Created on 2014年7月18日

@author: sony
'''
#连接本地数据库，用于本地数据库的管理
import MySQLdb
import traceback
# mysqldb_conn = MySQLdb.connect('localhost','root','12345')
# mysqldb_cursor = mysqldb_conn.cursor(MySQLdb.cursors.DictCursor)
DB_HOST='localhost'
DB_ADMIN_USER='root'
DB_ADMIN_PASSWD='12345'
class MysqlDBMgr(object):
	__DBNAMELIST=[]
	__MGR_COUNT=0
	__ADMIN_DB=['mysql','information_schema','performance_schema']
	def __init__(self):
		if MysqlDBMgr.__MGR_COUNT>=1:
			raise MgrNumberException()
		MysqlDBMgr.__MGR_COUNT=1
		self.mysqldb_conn = MySQLdb.connect(DB_HOST,DB_ADMIN_USER,DB_ADMIN_PASSWD)
		self.mysqldb_cursor = self.mysqldb_conn.cursor(MySQLdb.cursors.DictCursor)
		MysqlDBMgr.__DBNAMELIST=self.__getlocalaldbname()
		
	def __addelme_in_DBnamelist(self,rf_dbname):
		if rf_dbname.lower() in MysqlDBMgr.__ADMIN_DB:
			raise DBNoPermisionException()
		if rf_dbname in MysqlDBMgr.__DBNAMELIST:
			print 'run to this'
			raise DBExistsException()
		MysqlDBMgr.__DBNAMELIST.append(rf_dbname)
		
	def __delelme_in_DBnamelist(self,rf_dbname):
		index = 0
		if rf_dbname.lower() in MysqlDBMgr.__ADMIN_DB:
			raise DBNoPermisionException()
		for dbname in MysqlDBMgr.__DBNAMELIST:
			if dbname is rf_dbname:
				MysqlDBMgr.__DBNAMELIST.pop(index)
				break
			index+=1
				
				
	def __createdb(self,dbname):
		#添加的过程中有检验的过程所以必须先添加数据到DB列表中，并进行验证，如果通过才能真正的删除数据库
# 		self.__addelme_in_DBnamelist(dbname)
		try:
			rs = self.mysqldb_cursor.execute('create database if not exists %s' %dbname)
		except Exception,e:
			print e
# 			self.__delelme_in_DBnamelist(dbname)
			raise DBOperationException()
		
	
	def __deletedb(self,dbname):
		#删除的过程中有检验的过程所以必须先从DB列表中删除，并进行验证，如果通过才能真正的删除数据库
# 		self.__delelme_in_DBnamelist(dbname)
		try:
			self.mysqldb_cursor.execute('drop database %s' %dbname)
		except Exception,e:
			print e
# 			self.__addelme_in_DBnamelist(dbname)
			raise DBOperationException()
	
	def __ungrant_dbprivilege2user(self,dbname):
		try:
			self.mysqldb_cursor.execute('select User from mysql.db where host="%%" and db="%s"' %(dbname))
			users = self.mysqldb_cursor.fetchall()
			for user in users:
				db_username=user['User']
				self.mysqldb_cursor.execute('delete from mysql.db where Host="%%" and User="%s" and Db="%s"' %(db_username,dbname))
				rs = self.mysqldb_cursor.execute('select Host,Db,User from mysql.db where host="%%" and db!="%s" and User="%s"' %(dbname,db_username))
				if rs!=0: continue
				self.mysqldb_cursor.execute('delete from mysql.user where Host="%%" and User="%s"' %(db_username))
		except Exception,e:
			print traceback.format_exc()
			raise DBOperationException(e)
		
	def __create_user(self,db_username,db_passwd):
		try:
			self.mysqldb_cursor.execute('insert into mysql.user(Host,User,Password) values ("%%","%s",password(%s))' %(db_username,db_passwd))
			self.mysqldb_cursor.execute('FLUSH PRIVILEGES')
		except Exception,e:
			print e
			print traceback.format_exc()
			raise DBUserPrivilegesException()#处理用户已存在的问题
				
	def __grant_dbprivilege2user(self,db_username,db_passwd,dbname):
		
		try:
			rs = self.mysqldb_cursor.execute('grant all privileges on %s.* to %s@"%%" identified by "%s"' %(dbname,db_username,db_passwd))
			self.mysqldb_cursor.execute('FLUSH PRIVILEGES')
		except Exception,e:
			print e
			raise DBOperationException()#处理在授权过程中的错误问题
		return rs
	
	def __getlocalaldbname(self):
		self.mysqldb_cursor.execute('show databases')
		rs = self.mysqldb_cursor.fetchall()
		dbnamelist=[]
		for r in rs:
			dbnamelist.append(r['Database'])
		return dbnamelist
	def __check_user_passwd(self,db_username,db_passwd):
		try:
			rs = self.mysqldb_cursor.execute('select User,Password from mysql.user where user="%s" and Password=password("%s")' %(db_username,db_passwd))
			if rs!=0:
				return True
			return False
		except Exception,e:
			print traceback.format_exc()
			raise DBOperationException()
	def __is_user_exist(self,db_username):
		try:
			rs = self.mysqldb_cursor.execute('select User,Password from mysql.user where user="%s"' %(db_username))
		except Exception,e:
			print traceback.format_exc()
			raise DBOperationException()
		if rs!=0:
				raise UserExistsException('The Created user already exists')
		
	def __is_db_exist(self,dbname):
		try:
			rs = self.mysqldb_cursor.execute('select Db from mysql.db where Db="%s"' %dbname)
		except Exception,e:
			print traceback.format_exc()
			raise DBOperationException()
		if rs!=0:
				raise DBExistsException('The Created database already exists')
	def createdb4user(self,db_username,db_passwd,dbname):
		dbexcinfo={'errormsg':'unknowen error'}
		try:
			self.__is_db_exist(dbname)
			self.__is_user_exist(db_username)
			self.__create_user(db_username,db_passwd)
			self.__createdb(dbname)
			self.__grant_dbprivilege2user(db_username, db_passwd, dbname)
		except Exception,e:
			dbexcinfo['errormsg']=e.message
			return dbexcinfo
		dbexcinfo.clear()
		dbexcinfo['dbname']=dbname
		dbexcinfo['db_username']=db_username
		dbexcinfo['db_passwd']=db_passwd
		return dbexcinfo
		
	def deletedb4user(self,dbname):
		dbexcinfo = {'errormsg':'unknowen error'}
		try:
			self.__ungrant_dbprivilege2user(dbname)
			self.__deletedb(dbname)
		except Exception,e:
			print traceback.format_exc()
			dbexcinfo['errormsg']=e.message
			return dbexcinfo
		dbexcinfo.clear()
		dbexcinfo['dbname']=dbname
		return dbexcinfo

#测试
#mgr = MysqlDBMgr()
#print mgr.createdb4user('kinglong2', '12345', 'kingdb2')
#print mgr.deletedb4user('kingdb')
#print 'Done'
# def _createdb(dbname):
# 	rs = mysqldb_cursor.execute('show databases')
# 	
# 	rs = mysqldb_cursor.execute('create database if not exists %s' %dbname)
# 	return rs
# 
# def _grant_dbprivilege2user(db_username,db_passwd,dbname):
# 	rs = mysqldb_cursor.execute('grant all privileges on %s.* to %s@"%%" identified by "%s"' %(dbname,db_username,db_passwd))
# 	mysqldb_cursor.execute('FLUSH PRIVILEGES')
# 	return rs
# 
# def createdb4user(db_username,db_passwd,dbname):
# 	dbinfo={'errormsg':'error'}
# 	try:
# 		_createdb(dbname)
# 		_grant_dbprivilege2user(db_username, db_passwd, dbname)
# 	except Exception,e:
# 		print e
# 		dbinfo['errormsg']=e.message
# 	dbinfo.clear()
# 	dbinfo['dbname']=dbname
# 	dbinfo['db_username']=db_username
# 	dbinfo['db_passwd']=db_passwd
# 	return dbinfo
# 
# def deletedb(dbname):
# 	if dbname is 'mysql':
# 		raise 
# 	mysqldb_cursor.execute('drop database %s' %dbname)
# 	