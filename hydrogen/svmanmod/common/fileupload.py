#!/bin/python
import urllib2
class FileUpload(object):
	def __init__(self):
		pass
	def upload_file(self,vm_ip,contenttype,data):
		r = urllib2.Request("http://"+vm_ip+":8089/fileupload.app")
		r.add_unredirected_header('Content-Type',contenttype)
		r.add_data(data)
		u = urllib2.urlopen(r)
		return u
