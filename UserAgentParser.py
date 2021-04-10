#! /usr/bin/python3 

from user_agents import USER_AGENTS
import sys

available_ua = "Available: fu, fd, ff, fc, f7, f10, fan, fm, fi, cu, cf, ca, can, cm, ci, e7, e10, ean, em, ei"


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
        
        self.useragent = useragent.lower()
        self.user_agent_parser()


    def user_agent_parser(self):
        """
                Set User-Agent to default value from user_agents.py file, if specified user agent does not valid.
        """
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


        if   platform == 'u': platform = 'ubuntu'
        elif platform == 'f': platform = 'fedora'
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
        
        ######### DEBUGGING #########
        #print(browser)
        #print(platform)
        ######### END-DEBUGGING #########

        self.useragent = USER_AGENTS[browser][platform]

    
    def get_user_agent(self):
        return self.useragent


######### DEBUGGING ##########
#obj = UserAgentParser(sys.argv[1]).useragent
#print(obj)
######### END-DEBUGGING ##########