#!/usr/bin/python
#Filename: mysql.py

import MySQLdb
import os, sys

class Mysql(object):
	def __init__(self):
		self.conn = ''
		self.cursor  = ''
	def connect(self, host='localhost', user='root', passwd='12345', db='sc', charset='utf8'):
		try:
			self.conn = MySQLdb.connect(host, user, passwd, db)
		except Exception, e:
			print e
			sys.exit()
		self.cursor = self.conn.cursor()
	def insertMysql(self, sql):
		self.cursor.execute(sql)
		self.conn.commit()
	def query(self,sql):
		return self.cursor.execute(sql)
	def show(self):
		data=self.cursor.fetchall()
		for x in data:
			print x
	def get_nsid(self,sid):
		sql='select nsid from sct where sid=' + str(sid)
		self.cursor.execute(sql)
		data=self.cursor.fetchall()
		for x in data:
			return x
	def get_nsurl(self,sid):
		sql='select nsurl from sct where sid='+str(sid)
		self.cursor.execute(sql)
		data=self.cursor.fetchall()
		for x in data:
			return x
	def getvm_ip(self,vm_id):
		sql = 'select vm_ip from vmtb where vm_id='+vm_id
		self.cursor.execute(sql)
		data = self.cursor.fetchall()
		return data[0][0]
	def insertsvtb(self,sv_name,vm_id,user_id,sv_lang,sv_desc):
		sql = 'insert into sv_tb(sv_name,vm_id,user_id,sv_lang,sv_desc) values ("'+sv_name+'","'+vm_id+'","'+user_id+'","'+sv_lang+'","'+sv_desc+'");'
		#print sql
		self.cursor.execute(sql)
		sv_id = self.conn.insert_id()
		self.conn.commit()
		return str(sv_id)
	def updatesv_url(self,sv_id,sv_url):
		sql = 'update sv_tb set sv_url= "'+sv_url+'" where sv_id = "'+sv_id+'"'
		self.cursor.execute(sql)
		self.conn.commit()
	def insertsvargtb(self,arg_name,sv_id,arg_type_id,arg_index,arg_direct):
		sql = 'insert into sv_arg_type_tb(arg_name,sv_id,arg_type_id,arg_index,arg_direct) values ("'+arg_name+'","'+sv_id+'","'+arg_type_id+'","'+arg_index+'","'+arg_direct+'");'
		self.cursor.execute(sql)
		self.conn.commit()
	def querySvs(self):
		sql = 'select sv_tb.sv_id as sv_id,sv_name,authority_type,sv_url,vm_id,user_id,sv_lang,sv_desc,arg_name,sv_arg_type_tb.arg_type_id as arg_type_id,arg_index,arg_direct,arg_type_name from sv_tb,sv_arg_type_tb,arg_type_tb where sv_tb.sv_id=sv_arg_type_tb.sv_id and sv_arg_type_tb.arg_type_id = arg_type_tb.arg_type_id order by sv_id,arg_index;'
		return self.cursor.execute(sql)
			
	def close(self):
		self.cursor.close()
		self.conn.close()
	#def __del__(self):
	#	testfile=open('/printtxt.txt','w')
	#	stdout=sys.stdout
	#	stderr=sys.stderr
	#	sys.stdout=testfile
	#	sys.stderr=testfile
	#	print "close db_ins"
		#self.close()
