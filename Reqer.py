#! /usr/bin/python3

"""
    Capabilities: 
        - Accept target range ***
        - Port range***
        - Thread number (depends on list of URIs)***
        + File that contain http headers and parse it
        - Tamper http methods (bash version exist)
        + Tamper uesr agent header
        - Tamper http protocol version ???
        + Follow redirection

    Class Threads:
    	- Instantiate an object of 'Reqer' class
    	- Define number of threads
"""

from HeadersParser import RequestHeadersParser, ResponseHeadersParser
from PageScraper   import PageScraper
from config        import REQUEST_HEADERS
import requests as req
import re
import sys
import json


class Reqer:

	def __init__(self, target, redirect=None):

		self.result = {}
		self.redirect = redirect

		"""
			After preparation:
				- target: contain 'protocol schema' + 'hostname' + 'path' (http://example.com/path)
				- host: contain 'hostname' (example.com)
		"""
		self.target = target
		self.host   = target
		self.prepare_addresses()

		req_hp = RequestHeadersParser(self.host, REQUEST_HEADERS)
		self.request_headers = req_hp.get_headers()

		self.do_request()


	def do_request(self):
		"""
			Perform:
				- Do request 
				- Process response 
				- Update self.host and self.target and change the host header if redirection occured
		"""

		try:
			got_redirect = True

			while got_redirect:

				response = req.get(self.target, headers=self.request_headers, allow_redirects=False)
				self.response_processor(response)
				self.redirection_handler(response)
				got_redirect = response.is_redirect

		except Exception as e:
			print(e)


	def response_processor(self, response):
		"""
			Perform:
				- Parsing req/res headers
				- Scrape entire page (find links, comments, ...)
				- Indexing desired value
		"""

		res_hp = ResponseHeadersParser(response.headers)
		response_headers = dict( res_hp.get_headers() )
		request_headers  = dict( response.request.headers )

		ps = PageScraper( response.text )
		comments = ps.get_comments()
		links    = ps.get_links()
		tags     = ps.get_tags()

		self.result[response.request.url] = {}
		self.result[response.request.url]['status-code'] = response.status_code
		self.result[response.request.url]['req-headers'] = request_headers
		self.result[response.request.url]['res-headers'] = response_headers
		self.result[response.request.url]['comments']    = comments
		self.result[response.request.url]['links']       = links
		self.result[response.request.url].update(tags)


	def redirection_handler(self, response):
		"""
			Perform:
				- Update self.host and self.target values to location header if redirection occured
				- Prepare addresses
				- Change the value of the Host header
		"""

		self.target = response.headers['location']
		self.host   = response.headers['location']

		self.prepare_addresses()
		self.request_headers['Host'] = self.host


	def prepare_addresses(self):
		"""
			Perform:
				- Remove last forward slash
				- Check existence of protocol schema
				- Delete protocol schema and resource path from self.host
				- Adding protocol schema to self.target
		"""

		if self.target[-1] == '/':
			self.target = self.target[:-1]
			self.host   = self.host[:-1]

		pattern = "^http(s?)://"
		has_schema = re.match(pattern, self.target)

		if has_schema:
			self.host = re.sub(pattern, '', self.host).split('/')[0]
		else:
			self.target = f"http://{self.target}"


	def get_result(self):
		self.print_json( self.result )
		# return self.RESULT

	# TEST FUNCTION: prettify temporary output
	def print_json(self, data):
		print(json.dumps(data, indent=4))



##### DEBUGGING #####
if __name__ == "__main__":
	target = sys.argv[1]
	r = Reqer(target)
	r.get_result()
##### END-DEBUGGING #####