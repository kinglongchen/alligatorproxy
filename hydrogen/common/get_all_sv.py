#!/bin/python
'''
return the sv information as xml format:
for example:
<svs>
	<sv>
		<id></id>
		<name></name>
		<argtypes>
			<argtype>
				<type_id></type_id>
				<arg_index></arg_index>
				<type_name></type_name>
			</argtype>
			<argtype>...</argtype>
		<argtypes>
	</sv>
	<sv>...</sv>
	.
	.
	.
</svs>
'''
from dbop import Mysql
sv_xml = '<?xml version="1.0" encoding="utf-8"?>\n'
sv_xml += '<svs>\n'
sql_conn = Mysql()
sql_conn.connect()
sql = 'select svtb.sv_id,sv_name,svargtb.type_id,arg_index,typename from svtb,svargtb,argtypestb where svtb.sv_id = svargtb.sv_id and svargtb.type_id = argtypestb.type_id order by sv_id,arg_index;'
data = sql_conn.query(sql)
old_sv_id = -1
for x in data:
	sv_id = x[0]
	if sv_id != old_sv_id:
		if old_sv_id != -1:
			sv_xml += '</argtypes>\n'
			sv_xml += '</sv>\n'
		sv_xml += '<sv>\n'
		sv_xml += '<id>'+str(x[0])+'</id>\n'
		sv_xml += '<name>'+str(x[1])+'</name>\n'
		sv_xml += '<argtypes>\n'
		old_sv_id = sv_id
	sv_xml += '<argtype>\n'
	sv_xml += '<type_id>'+str(x[2])+'</type_id>\n'
	sv_xml += '<arg_index>'+str(x[3])+'</arg_index>\n'
	sv_xml += '<type_name>'+str(x[4])+'</type_name>\n'
	sv_xml += '</argtype>\n'
sv_xml += '</argtypes>\n'
sv_xml += '</sv>\n'
sv_xml += '</svs>\n'
sql_conn.close()
print sv_xml
