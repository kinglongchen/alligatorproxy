#encoding: utf-8
'''
Created on 2014��6��24��

@author: sony
'''
import logging
import os
import traceback
Verbose=True
Debug=True
# log_dire='c:\\log\\ceeas\\'
log_dire='/var/log/alligatorproxy/'

if not os.path.exists(log_dire):
	os.makedirs(log_dire)
	
msg_log_name='msg.log'
error_log_name='error.log'
msg_log_path=log_dire+msg_log_name
error_log_path=log_dire+error_log_name


# msg_log_file=file(msg_log_path,'w')
# error_log_file=file(error_log_path,'w')



logger = logging.getLogger(__name__)
fmt = logging.Formatter('%(name)-12s %(asctime)s %(levelname)-8s %(message)s', '%a, %d %b %Y %H:%M:%S',)
msg_file_handler=logging.FileHandler(msg_log_path)
error_file_handler=logging.FileHandler(error_log_path)
stdout_handler = logging.StreamHandler()

msg_file_handler.setFormatter(fmt)
error_file_handler.setFormatter(fmt)
stdout_handler.setFormatter(fmt)

msg_file_handler.setLevel(1)
error_file_handler.setLevel(logging.ERROR)
stdout_handler.setLevel(1)


#file_handler.setFormatter(fmt)
logger.addHandler(msg_file_handler)
logger.addHandler(error_file_handler)
if Verbose:
	logger.addHandler(stdout_handler)
logger.setLevel(1)

def debug(*args,**kwargs):
	if Debug:
		logger.debug(*args,**kwargs)

def info(*args,**kwargs):
	if Debug:
		logger.info(*args,**kwargs)
		
def warning(*args,**kwargs):
	if Debug:
		logger.warning(*args,**kwargs)
		
def error(*args,**kwargs):
	if Debug:
		logger.error(*args,**kwargs)
		track_msg = traceback.format_exc()
		logger.error(track_msg)	
			
def critical(*args,**kwargs):
	if Debug:
		logger.critical(*args,**kwargs)
		track_msg = traceback.format_exc()
		logger.error(track_msg)