# Super models are extended versions of db.Model which allow for option
# __in__ and __out__ fields which are arbitrary functions to coerse data
# into the underlying model
from google.appengine.ext import db
from django.utils import simplejson as json
import logging
	
reserved_fields = ['to_json', 'all','app','copy','delete','entity','entity_type','fields','from_entity','get','gql','instance_properties','is_saved','key','key_name','kind','parent','parent_key','properties','put','setdefault','to_xml','update']
ERROR = 'supermodelpy_error_code'

class SuperModel(db.Model):	
	def to_json(self):
		jdict = {}
		for field in self.fields():
			jdict[field] = str(getattr(self, field))
		return json.dumps(jdict)
	def __setattr__(self, key, value):
		if key[0] != '_' and key not in reserved_fields:
			logging.debug('set ' + key)
			try:
				if self.__auth__.has_key(key):
					auth_func = self.__auth__[key]['w']
					authorized = auth_func(self)
				else:
					authorized = True
				logging.debug(authorized)
				if authorized:
					super(db.Model, self).__setattr__(key, value)
				else:
					raise Exception("You dont have write permissions")
			except AttributeError:
				super(db.Model, self).__setattr__(key, value)
		else:
			super(db.Model, self).__setattr__(key, value)

	def __getattribute__(self, key):
		if key[0] != '_' and key not in reserved_fields:
			logging.debug('get ' + key)
			try:
				if self.__auth__.has_key(key):
					auth_func = self.__auth__[key]['r']
					authorized = auth_func(self)
				else:
					authorized = True
				logging.debug(authorized)
				if authorized:
					return super(db.Model, self).__getattribute__(key)
				else:
					raise Exception("You dont have read permissions")
			except AttributeError:
				return super(db.Model, self).__getattribute__(key)
		else:
			return super(db.Model, self).__getattribute__(key)

def POST(sm, **data):
	fields = [field for field in dir(sm) if field[0] != '_' and field not in reserved_fields]
	errors = []
	for key in data: 
		if sm.__dict__.has_key('__in__'): 
			if sm.__in__.has_key(key): 
				data_entry = sm.__in__[key](data[key])
				if isinstance(data_entry, list):
					if data_entry[0] is ERROR:
						errors.append(data_entry[1])
				data[key] = data_entry
		if key[0] != '_' and key not in reserved_fields:
			logging.debug('start set ' + key)
			try:
				if sm.__auth__.has_key(key):
					auth_func = sm.__auth__[key]['w']
					authorized = auth_func(sm)
				else:
					authorized = True
				logging.debug(authorized)
				if authorized:
					pass
				else:
					raise Exception("You dont have write permissions")
			except AttributeError as e:
				logging.debug(e)
		else:
			pass
	if len(errors) is 0:
		instance = sm(**data)
		instance.put()
		return str(instance.key()), None
	else:	
		return None, errors

def PUT(sm, key, **data):
	model = sm.get(key)
	for name in data:
		if sm.__dict__.has_key('__in__'): 
			if sm.__in__.has_key(name) and data[name]: data[name] = sm.__in__[name](data[name])
		setattr(model, name, data[name])
	model.put()
	return model

def GET(sm, key):
	model = sm.get(key)
	return model

def DELETE(sm, key):
	model = sm.get(key)
	model.delete()
	return True