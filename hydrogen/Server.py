#! /usr/bin/env python2.7
#encoding:utf-8
#@description:һ¸öhonÊ»¤½øÀ×
#@tags:python,daemon
import sys
import os
from paste.deploy import loadapp
sys.path.append(os.path.split(os.getcwd())[0]) 
HOST = ''
PORT = 8091
config = os.getcwd()+"/python_paste.ini"
appname = "common"
print os.popen('pwd').readlines()[0]
application = loadapp("config:%s" % os.path.abspath(config), appname)
