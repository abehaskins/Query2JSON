#!/usr/bin/env python
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import util
from django.utils import simplejson as json
import urllib2

import sys
sys.path.insert(0, 'lib')
from supermodel import *
from bottle import *
import bottle


domain = "http://www.query2json.com/"

# Link Model
class Link(SuperModel):
	url 			= db.StringProperty(required=True)
	response 		= db.StringProperty()

# Create a new Link
@route("/new/")
def get():
	l = Link(url=bottle.request.query.url, response=bottle.request.query.response)
	l.put()
	return json.dumps({"url": domain + str(l.key())})	

# Use a Link
@route("/:tid")
def get(tid=None):
	l = Link.get(tid)
	if l:
		url = l.url
		jsoned = json.dumps(dict(request.GET)) 
		result = urllib2.urlopen(url, jsoned)
		response = l.response
		if response is '':
			return jsoned
		else:
			return response
	else:
		bottle.response.status = 404
		return ''

# Run the app
def main():
	run_wsgi_app(default_app())

if __name__ == '__main__':
    main()
