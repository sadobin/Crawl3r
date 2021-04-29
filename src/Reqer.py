#! /usr/bin/python3

import requests as req
import json
import re
import sys, os
sys.path.append( os.path.dirname( os.path.realpath(__file__) ) )

from PageScraper    import PageScraper
from HeadersParser import RequestHeadersParser, ResponseHeadersParser



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

		req_hp = RequestHeadersParser(self.host)
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

				response = req.get(
					self.target, 
					headers=self.request_headers, 
					allow_redirects=False, 
					timeout=5
					)

				got_redirect = response.is_redirect

				self.response_processor(response)

				if got_redirect:
					self.redirection_handler(response)

		except Exception as e:
			alert = "\33[31m[!]\33[0m"
			print(f"{alert} Reqer: {e} ({self.target})")


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
		self.result[response.request.url]['status-code']      = response.status_code
		self.result[response.request.url]['request-headers']  = request_headers
		self.result[response.request.url]['response-headers'] = response_headers
		self.result[response.request.url]['comments']         = comments
		self.result[response.request.url]['links']            = links
		self.result[response.request.url].update(tags)


	def redirection_handler(self, response):
		"""
			Perform:
				- Update self.host and self.target values to location header if redirection occured
				- Prepare addresses
				- Change the value of the Host header
		"""

		location = response.headers.get('location')

		if location:

			if re.match('^http(s?):\/\/', location):
				self.target = location
				self.host   = location

			else:
				if location.startswith("/"):
					self.target = "".join( i for i in self.target.split("/")[0:3] )
					self.target = self.target.replace(":", "://")
					self.target += location


		self.prepare_addresses()
		self.request_headers['Host'] = self.host


	def prepare_addresses(self):
		"""
			Perform:
				- Delete protocol schema and resource path from self.host
				- Adding protocol schema to self.target
		"""

		schema_pattern = "^http(s?):\/\/"

		if re.match(schema_pattern, self.host):
			self.host = re.sub(schema_pattern, '', self.host).split('/')[0]

		else:
			self.host = self.host.split('/')[0]


		if not re.match(schema_pattern, self.target):
			self.target = f"http://{self.target}"


	def get_result(self):
		# Return crawling result and hostname
		if __name__ == "__main__":
			print( json.dumps(self.result, indent=4) )
		else:
			return self.result



##### DEBUGGING #####
if __name__ == "__main__":
	target = sys.argv[1]
	r = Reqer(target)
	r.get_result()
##### END-DEBUGGING #####
