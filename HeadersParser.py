#! /usr/bin/python3

from UserAgentParser import UserAgentParser
from PageScraper import PageScraper
from config import REQUEST_HEADERS, RESPONSE_HEADERS
import json


class RequestHeadersParser:

    def __init__(self, host):
        self.host    = host
        self.headers = REQUEST_HEADERS

        self.headers_parser()


    def headers_parser(self):
        self.check_host_header()
        self.check_user_agent_header()


    def check_host_header(self):
        if self.headers['Host'] == 'TARGET':
            self.headers['Host'] = self.host


    def check_user_agent_header(self):
        ua = UserAgentParser( self.headers['User-Agent'] )
        self.headers['User-Agent'] = ua.get_user_agent()

    
    def get_headers(self):
        return self.headers



class ResponseHeadersParser:

    def __init__(self, res_headers):

        """
            Define desired response headers to be indexed in RESPONSE_HEADERS.
            All response headers would be indexed if the RESPONSE_HEADERS has no value.
        """

        self.headers = {}

        if RESPONSE_HEADERS and RESPONSE_HEADERS[0]:
            for header in RESPONSE_HEADERS:
                self.headers.update( self.fetch_header(res_headers, header) )
        else:
            self.headers = res_headers


    def fetch_header(self, res_headers, header_name):
        if res_headers.get(header_name):
            return { header_name: res_headers.get(header_name) }
        else:
            return {}


    def get_headers(self):
        return self.headers
