#encoding: utf-8
'''
Created on 2014��7��14��

@author: sony
'''
import dbop
db_session=dbop.Mysql()
db_session.connect()
def get_sv_ip(sv_id):
	sql='select sv_url from sv_tb where sv_id="'+str(sv_id)+'"'
	rs = db_session.query(sql)
	if not rs:
		raise BadServiceIDException(sv_id=id)
	sv_url = rs[0]['sv_url']
	return sv_url

#print get_sv_ip(60)