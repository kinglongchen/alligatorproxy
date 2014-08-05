#encoding:utf-8
'''
Created on 2014年7月14日

@author: sony
'''
# import sys
# sys.path.append('/root/alligatorproxy/')
import time
import httplib2
import json
from hydrogen.common import db
def request(sv_id,reqargs):
	reqargs=json.dumps(reqargs)
	sv_id=str(sv_id)
	svurl=db.get_sv_ip(sv_id)#   通过sv_id获取对应sv_id服务的URL
	httpClient=httplib2.Http()
	resp,content=httpClient.request(svurl,'POST',body=reqargs,headers={'Content-Type':'application/json'})
	print content
	rsargs=json.loads(content)
	return rsargs

# def request(sv_id,reqargs):
# 	a=reqargs.get('a')
# 	a+=100
# 	print a
# 	if a>1000:
# 		reqargs['ckey']=False
# 	reqargs['a']=a
# 	return reqargs

def exc(svcj,reqargs):
	if svcj is None:
		raise NullSvcJsonError()
	key=svcj.keys()[0]
	value=svcj.get(key,None)
	if key == 'sv':
		sv_id=value.get('id',None)
		okwargs=value.get('okwargs',None)
		if okwargs:
			reqargs.update(okwargs)
		reqargs=request(sv_id,reqargs)
		return reqargs
	
	if key == 'sequence':
		for svcsubj in value:
			reqargs = exc(svcsubj,reqargs)
		return reqargs
	
	if key == 'if':
		ckey=value.get('ckey',None)
		if not ckey:
			raise NullConditionError()
		condition = reqargs.get(ckey,None)
# 		if condition is None:
# 			raise NullConditionError()
		if condition == 'True' or condition == 'true' or condition is True:
			svcsubj = value.get('true',None)
		elif condition == 'False' or condition == 'false' or condition is False or condition is None:
			svcsubj=value.get('false',None)
		else:
			raise ErrorBooleanException()
		if svcsubj:
			reqargs = exc(svcsubj,reqargs)
		return reqargs
	
	if key == 'switch':
		ckey=value.get('ckey',None)
		if not ckey:
			raise NullConditionError()
		condition = reqargs.get(ckey,None)
		if not condition:
			condition='default'
		case = value.get('case',None)
		svcsubj = case.get(condition,None)
		if svcsubj:
			reqargs = exc(svcsubj,reqargs)
			
		return reqargs
	
	if key == 'while':
		ckey=value.get('ckey',None)
		sleeptime=int(value.get('sleeptime',0))
		if not ckey:
			raise NullConditionError()
		condition = reqargs.get(ckey,None)
		if condition is None:
			print 'no ckey'
			pass#从其他方面获取while循环的条件
		
		while condition == 'True' or condition == 'true' or condition is True:
			svcsubj = value.get('body',None)
			if svcsubj:
				reqargs = exc(svcsubj,reqargs)
			else:
				return reqargs
			if sleeptime:
				time.sleep(sleeptime)
			condition = reqargs.get(ckey,None)
			
		#print str(condition) is 'true'
		if condition == 'False' or condition == 'false' or condition is None or condition is False:
			return reqargs
		else:
			raise ErrorBooleanException()
			#exc(svcj,reqargs)#循环执行while块
			
#	if key == ''
			
#测试

#print request(62, '{"scatdataline":"0;0;1"}')
#sv测试
#svcj={'sv':{'id':'1','okwargs':{'a':1,'b':0}}}


#if测试
'''
svcj={'if':{'ckey':'ckey',
		'true':{'sv':{'id':'1','okwargs':{'a':1,'b':0}}},
		'false':{'sv':{'id':'2','okwargs':{'a':1,'b':0}}},
		}
	
	}
'''

#sequence测试
'''
svcj={
	'sequence':[
			{'sv':{'id':'1'}},
			{'sv':{'id':'2'}},
			{'sv':{'id':'3'}},
			{'sv':{'id':'4'}}
			]
	
	}
'''
#while测试
'''
svcj={
	'while':{'ckey':'ckey',
			'sleeptime':1,
			'body':{'sv':{'id':'1'}}
			
			}
	}
reqargs={'ckey':True,'a':0}	
'''
#switch测试
'''
svcj={'switch':{'ckey':'ckey',
				'case':{
					'sv_1':{'sv':{'id':'1'}},
					'sv_2':{'sv':{'id':'2'}},
					'sv_3':{'sv':{'id':'3'}}
					}
			
			}
	}
'''
#解析服务swith的一个例子
'''
svcj={'switch':{'ckey':'ckey',
				'case':{
					'sv_1':{'sv':{'id':'60'}},
					'sv_2':{'sv':{'id':'61'}},
					'sv_3':{'sv':{'id':'62'}}
					}
			}
	}
'''
#顺序结构组合的一个列子
'''
svcj={'sequence':[
				{'sv':{'id':63}},
				{'sv':{'id':64}},
				{'sv':{'id':65}}
				]
	}

reqargs={'line':'1;2;3#3;4;5'}
'''


#while循环结构组合的一个例子
'''
svcj={'while':{'ckey':'ckey',
			'sleeptime':1,
			'body':{'sv':{'id':66}}
			}
	}

reqargs={'ckey':'true','a':'0'}
'''

#if逻辑结构的一个例子
'''
svcj={'if':{'ckey':'ckey',
			'true':{'sv':{'id':67}},
			'false':{'sv':{'id':68}}
			}
	}
reqargs={'a':'0'}
'''
#print exc(svcj,reqargs)
		
			
	
	
	