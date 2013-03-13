#!/usr/bin/env python
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import util
from django.utils import simplejson as json
from supermodel import *
from bottle import *
import bottle
import urllib2

# Link Model
class Link(SuperModel):
	url 			= db.StringProperty(required=True)
	response 		= db.StringProperty(required=True)

# Home Page
@route("/")
def get():
	return "My swag worth a billion"

# Create a new Link
@route("/new/")
def get():
	l = Link(url=bottle.request.query.url, response=bottle.request.query.response)
	l.put()
	return str(l.key())

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
