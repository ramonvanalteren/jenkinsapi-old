import StringIO
import requests

class Requester(object):

	"""
	A class which carries out HTTP requests. You can replace this class with one of your own implementation if you require
	some other way to access Jenkins.

	This default class can handle simple authentication only.
	"""

	def __init__(self, username=None, password=None):
		if username:
			assert password, 'Cannot set a username without a password!'

		self.username = None
		self.password = None

	def hit_url(self, url, params=None, data=None, headers=None):
		requestKwargs = {}
		if self.username:
			requestKwargs['auth'] = (self.username, self.password)

		if params:
			assert isinstance(params, dict), 'Params must be a dict, got %s' % repr(params)
			requestKwargs['params'] = params

		if headers:
			assert isinstance(headers, dict), 'headers must be a dict, got %s' % repr(headers)
			requestKwargs['headers'] = headers

		if data:
			requestKwargs['data'] = data
			response = requests.post(url, **requestKwargs)
		else:
			response = requests.get(url, **requestKwargs)

		import ipdb; ipdb.set_trace()

		return response.text
