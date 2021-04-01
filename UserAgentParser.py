#! /usr/bin/python3 

from USER_AGENTS import USER_AGENTS
import sys


class UserAgentParser :

    """
        User Agent format: BROWSER-PLATFORM

        FIREFOX:
            - fu, fd, ff, fc
            - f7, f10
            - fan
            - fm
            - fi

        CHROME:
            - cu, cf, ca
            - c7, c10
            - can
            - cm
            - ci

        EDGE:
            - e7, e10
            - ean
            - em
            - ei
        
        Availables:
            - fu, fd, ff, fc, f7, f10, fan, fm, fi, cu, cf, ca, can, cm, ci, e7, e10, ean, em, ei
    """

    def __init__(self, useragent):
        
        self.err       = "[!] Unsupported __STR__"
        self.available = "[+] Available: fu, fd, ff, fc, f7, f10, fan, fm, fi, cu, cf, ca, can, cm, ci, e7, e10, ean, em, ei"
        self.useragent = useragent.lower()
        self.user_agent_parser()

        ######### DEBUGGING #########
        # print( USER_AGENTS['firefox']['ubuntu'] )
        # print(USER_AGENTS['chrome'])
        # print(USER_AGENTS['edge'])
        ######### END-DEBUGGING #########
    

    def user_agent_parser(self):

        if not self.useragent:
            self.useragent =  USER_AGENTS['default']
            return
        
        browser  = self.useragent[0]
        platform = self.useragent[1:]

        if   browser == 'f': browser = 'firefox'
        elif browser == 'c': browser = 'chrome'
        elif browser == 'e': browser = 'edge'
        else:
            self.useragent = USER_AGENTS['default']
            return
            #print( self.err.replace('__STR__', 'browser') )
            #print( self.available )
            #sys.exit(1)

        if   platform == 'u': platform = 'ubuntu'
        elif platform == 'f': platform = 'firefox'
        elif platform == 'c': platform = 'centos'
        elif platform == 'd': platform = 'debian'
        elif platform == 'a': platform = 'arch'
        elif platform == '7': pass
        elif platform == '10': pass
        elif platform == 'an': platform = 'android'
        elif platform == 'm': platform = 'mac'
        elif platform == 'i': platform = 'ios'
        else: 
            self.useragent = USER_AGENTS['default']
            return
            #print( self.err.replace('__STR__', 'platform') )
            #print( self.available )
            #sys.exit(1)
        
        ######### DEBUGGING #########
        #print(browser)
        #print(platform)
        ######### END-DEBUGGING #########

        self.useragent = USER_AGENTS[browser][platform]


######### DEBUGGING ##########
#obj = UserAgentParser(sys.argv[1]).useragent
#print(obj)
######### END-DEBUGGING ##########