#! /usr/bin/python3 
import subprocess, os, sys

"""
    Depth of crawling
    E.g: If it was set to 2, passed URL and all found links in it will be crawled.
    Assigning 0 to it, causing crawling the entire domain.
"""
DEPTH = 0


"""
    Number of processes
"""
PROCESSES = 12


"""
    Path to save the result
"""
home_dir = subprocess.check_output( 'echo $HOME', shell=True ).decode().strip()
if not os.path.exists(f"{home_dir}/crawl3r"):
    os.system(f"mkdir {home_dir}/crawl3r")
RESULT_PATH = f"{home_dir}/crawl3r"


"""
    Put desired request headers
     - If Host header was set to TARGET, the hostname of target will be assigned to Host header during requests.
     - Choose appropriate User-Agent header from user_agents.py file.
"""
REQUEST_HEADERS = {

    'Host': 'TARGET',
    'User-Agent': 'w7',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.5',
    'Connection': 'keep-alive',
    # 'DNT': '1',
    #'Cache-Control': 'max-age=0',
    #'Upgrade-Insecure-Requests': '1',

}


"""
    Specify desired response headers to be indexed.
"""
RESPONSE_HEADERS = [
    '',
]


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
    'form',
    ]
