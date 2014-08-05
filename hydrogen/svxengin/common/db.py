#encoding: utf-8
'''
Created on 2014年7月14日

@author: sony
'''
# import sys
# sys.path.append('/root/alligatorproxy/')
from hydrogen.common import dbop
def get_sv_ip(db_session,sv_id):
	sql='select sv_url from sv_tb where sv_id="'+str(sv_id)+'"'
	rs = db_session.query(sql)
	if not rs:
		raise BadServiceIDException(sv_id=id)
	sv_url = rs[0]['sv_url']
	return sv_url

# db_session=dbop.Mysql()
# db_session.connect()
# print get_sv_ip(db_session,60)