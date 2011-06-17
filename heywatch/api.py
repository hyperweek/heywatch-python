import httplib2
import urllib
import json
import re

class BadRequest(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)

class API:		
	def __init__(self, username, password):
		self.url = 'http://heywatch.com'
		self.cli = httplib2.Http()
		self.cli.add_credentials(username, password)
		
		self.headers = {'Accept': 'application/json',
		 'User-Agent': 'HeyWatch py/1.0.0'
		}
		
		self.account()
		
	def account(self):
		return self.request('/account')
		
	def info(self, resource, id):
		return self.request('/' + resource + '/' + str(id))
	
	def jpg(self, id, **params):
		if(params.has_key('async')):
			params.pop('async')
			self.request('/encoded_video/' + str(id) + '/thumbnails', 'POST', body=urllib.urlencode(params))
			return True
			
		if(len(params) > 0):
			params = '?' + urllib.urlencode(params)
		else:
			params = ''
		
		return self.request('/encoded_video/' + str(id) + '.jpg' + params)
	
	def bin(self, resource, id):
		self.cli.follow_redirects = False
		response, content = self.cli.request(self.url + '/' + resource + '/' + str(id) + '.bin', 'GET')
		self.cli.follow_redirects = True
		return self.cli.request(response['location'], 'GET')[1]
		
	def all(self, resource):
		return self.request('/' + resource)

	def count(self, resource):
		return len(self.all(resource))
		
	def create(self, resource, **data):
		return self.request('/' + resource, 'POST', body=urllib.urlencode(data))

	def update(self, resource, id, **data):
		return self.request('/' + resource + '/' + str(id), 'PUT', body=urllib.urlencode(data))
		
	def delete(self, resource, id):
		return self.request('/' + resource + '/' + str(id), 'DELETE')
		
	def request(self, resource, method='GET', **args):
		params = {'headers':self.headers}
		params.update(args)

		response, content = self.cli.request(self.url + resource, method, **params)
		
		if(re.search('^4|5', response['status'])):
			raise BadRequest(response['status'] + " " + content)
			
		if(len(content) > 0 and re.search('json', response['content-type'])):
			return json.loads(content)
		else:
			return content