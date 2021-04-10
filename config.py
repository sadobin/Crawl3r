#! /usr/bin/python3 

"""
    Put desired request headers
     - If Host header was set to TARGET, the hostname of target will be assigned to Host header during requests.
     - Choose appropriate User-Agent header from user_agents.py file.
"""

REQUEST_HEADERS = {

    'Host': 'TARGET',
    'User-Agent': 'ff',
    'Accept': '*/*',
    'Accept-Encoding': '',
    'Connection': 'keep-alive',

}


"""
    Define html attributes which contain uri (in regex format).
    Check following discussion:
        - https://stackoverflow.com/questions/2725156/complete-list-of-html-tag-attributes-which-have-a-url-value
    
"""

HTML_ATTRIBUTES = '(href|src|action)'


"""
    Specify desired tag to be indexed.
"""

HTML_TAGS = [
    'meta',
    ]