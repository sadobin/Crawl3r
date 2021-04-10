#! /usr/bin/python3

from UserAgentParser import UserAgentParser
from PageScraper import PageScraper
import json


class RequestHeadersParser:

    def __init__(self, host, headers):
        self.host    = host
        self.headers = headers

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
            Define desired response headers to be indexed.
        """

        # Nothing to do 
        self.res_headers = res_headers


    def get_headers(self):
        return self.res_headers
