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
	def insertsvtb(self,svname,user_id,sv_ip,sv_port):
		sql = 'insert into svtb(sv_name,user_id,sv_ip,sv_port) values ("'+svname+'","'+user_id+'","'+sv_ip+'","'+sv_port+'");'
		#print sql
		self.cursor.execute(sql)
		sv_id = self.conn.insert_id()
		self.conn.commit()
		return str(sv_id)
	def updatesv_url(self,sv_id,sv_url):
		sql = 'update svtb set sv_url= "'+sv_url+'" where sv_id = "'+sv_id+'"'
		self.cursor.execute(sql)
		self.conn.commit()
	def insertsvargtb(self,sv_id,arg_index,type_id):
		sql = 'insert into svargtb(sv_id,arg_index,type_id) values ("'+sv_id+'","'+str(arg_index)+'","'+type_id+'");'
		self.cursor.execute(sql)
		self.conn.commit()
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
