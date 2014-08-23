#encoding: utf-8
'''
Created on 2014年8月7日

@author: sony
'''

import MySQLdb
import os, sys
import configparser

SV_TB='sv_tb'
SV_INST_TB='sv_inst_tb'
SV_POLICY_TB='sv_policy_tb'
SERVER_TB='vm_overview'

class Mysql(object):
	def __init__(self):
		self.conn = ''
		self.cursor  = ''
	def connect(self, host='192.168.0.12', user='root', passwd='12345', db='sv_db', charset='utf8'):
		try:
			self.conn = MySQLdb.connect(host, user, passwd, db)
		except Exception, e:
			print e
			sys.exit()
		self.cursor = self.conn.cursor(MySQLdb.cursors.DictCursor)
	
	def execute4DML(self,sql):
		self.cursor.execute(sql)
		id = self.conn.insert_id()
		self.conn.commit()
		return id
	def execute4DQL(self,sql):
		self.cursor.execute(sql)
		return self.cursor.fetchall()
	def query(self,sql):
		return self.execute4DQL(sql)
	def insert(self, sql):
		return self.execute4DML(sql)
	def delete(self,sql):
		return self.execute4DML(sql)
	def update(self,sql):
		return self.execute4DML(sql)
	
	def queryInfo(self,tb,fileds,codis):
		fileds_sql = ','.join(fileds)
# 		codis_sql = 'where '+' and '.join('%s=%s'%(key,codis[key]) for key in codis.keys()) if codis else ''
		time_span=None
		
		if codis:
			#下面的代码是对前面修改之前代码的兼容的处理
			#{'a':'1','b':'2'}
			if isinstance(codis,dict):
				temp_d = []
				for key in codis.keys():
					if not isinstance(codis[key],list):
						codis[key]=[codis[key]]
					temp_d.append({key:codis[key]})
				codis=temp_d
			
# 			for codi in codis:
# 				if 'time_span' in codi:
# 					time_span = codi.pop('time_span')
# 					break
			
			for i in range(len(codis)):
				if 'time_span' in codis[i]:
					time_span=codis[i].pop('time_span')
					if not codis[i]:
						del codis[i]
					break
				
				
					
		
						
			############################################################
			##########################################################
# 			time_span=codis.pop('time_span',None)
		
		codis_sql = 'where '+' and '.join('(%s)' %' or '.join('(%s)' %' or '.join("%s='%s'" %(key,val)  for val in codi[key])  for key in codi.keys()) for codi in codis ) if codis else ''
		
		if time_span:
				time_sql='unix_timestamp(create_time) between unix_timestamp(%s) and unix_timestamp(%s)' %tuple(time_span)
				codis_sql='%s and %s' %(codis_sql,time_sql)
		
		sql = 'select %s from %s %s' %(fileds_sql,tb,codis_sql)
# 		print sql
		return self.query(sql)
	
	def insertInfo(self,tb,kwvals):
		fileds_sql=','.join(kwvals.keys())
		values_sql=','.join('%s' %val for val in kwvals.values())
		sql = 'insert into %s(%s) values (%s)' %(tb,fileds_sql,values_sql)
		id = self.insert(sql)
		return id
	
    	 
	def updateInfo(self,tb,kwvals,codis):
# 		if len(codis) == 0:raise Exception('Warning:Update Condition can not be None')
		kwval_sql = ','.join('%s=%s' %(key,kwvals[key]) for key in kwvals.keys())
		codis_sql = ' and '.join('%s=%s' %(key,codis[key]) for key in codis.keys())
		sql = 'update %s set %s where %s' %(tb,kwval_sql,codis_sql)
		return self.update(sql)
	
	def deleteInfo(self,tb,codis):
		codis_sql = ' and '.join('%s=%s' %(key,codis[key]) for key in codis.keys())
		sql = 'delete from %s where %s' %(tb,codis_sql)
		return self.delete(sql)
	
	def insertsvargtb(self,arg_name,sv_id,arg_type_id,arg_index,arg_direct):
		sql = 'insert into sv_arg_type_tb(arg_name,sv_id,arg_type_id,arg_index,arg_direct) values ("'+arg_name+'","'+sv_id+'","'+arg_type_id+'","'+arg_index+'","'+arg_direct+'");'
		self.cursor.execute(sql)
		self.conn.commit()
	
			
	def close(self):
		self.cursor.close()
		self.conn.close()


db_config = configparser.cfg.get_DB_config()
host = db_config['host']
user = db_config['user']
passwd = db_config['passwd']
db = db_config['db']
charset = db_config['charset']
db_session = Mysql()
db_session.connect(host=host, user=user, passwd=passwd, db=db, charset=charset)		
# db = Mysql()
# db.connect()
# rs = db.query('select * from sv_tb')
# for r in rs:
# 	print r
	#def __del__(self):
	#	testfile=open('/printtxt.txt','w')
	#	stdout=sys.stdout
	#	stderr=sys.stderr
	#	sys.stdout=testfile
	#	sys.stderr=testfile
	#	print "close db_ins"
		#self.close()
