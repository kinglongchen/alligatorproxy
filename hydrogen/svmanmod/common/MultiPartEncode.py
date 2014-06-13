#!/bin/python
import mimetools, mimetypes
class MultiPartEncode(object):
	def __init__(self):
		self.svname = "svname"
	def encode(self,sv_filename,sv_file,boundary):
		contenttype = mimetypes.guess_type(sv_file.filename)[0] or 'application/octet-stream'
		buffer = ''
		buffer += '--%s\r\n' % boundary
		buffer += 'Content-Disposition: form-data; name="%s"; filename="%s"\r\n' % (sv_file.name, sv_filename)
		buffer += 'Content-Type: %s\r\n' % contenttype
		buffer += '\r\n' + sv_file.value + '\r\n'
		buffer += '--%s--\r\n\r\n' % boundary
		return buffer
