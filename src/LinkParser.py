#! /usr/bin/python3

from collections import Counter
from urllib.parse import urlparse
import html
import re
import sys
import json


class LinkParser:

    def __init__(self, reqer_result):

        try:
            self.links        = []
            self.static_files = []
            self.reqer_result = reqer_result

            self.prepare_links()
            self.links = list( Counter(self.links).keys() )     # Put away duplicate links
            self.find_static_files()

        except Exception as e:
            print(f"[!] LinkParser: {e}")
            sys.exit(1)
    

    def prepare_links(self):

        """
            Prepare links for next crawl
        """

        for url in self.reqer_result:
            """
                host: hostname with subdomains (e.g: sub1.sub2.example.com)
                target: orginal hostname which does not contain subdomains (e.g: example.com)
            """

            parsed_url = urlparse(url)
            host = parsed_url.hostname

            ip_regex = "[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}"
            if re.search(f'{ip_regex}(\/)?$', host):
                target = re.search(f'{ip_regex}(\/)?$', host).group()
            else:
                target = re.search('[0-9a-zA-Z-]+\.[0-9a-zA-Z-]+$', host).group()

            for link in self.reqer_result[url]['links']:

                parsed_link = urlparse(link)

                link = link.replace(f'#{parsed_link.fragment}', '')
                link = html.unescape(link)

                # Ignore special protocols
                if re.search( '^(mailto:|tel:|javascript:|data:|android-app:|ios-app:|\{)', link ):
                    pass

                elif 'http' in parsed_link.scheme:
                    if target in parsed_link.hostname:
                        self.links.append(link)

                elif re.search('^\/\/', link):
                    if target in parsed_link.hostname:
                        temp_link = parsed_url.scheme + "://" + link[2:]
                        self.links.append(temp_link)

                # Append link to the current url
                elif re.search('^(\.\.|\/\.\.)', link):
                    temp = f'{parsed_url.scheme}://' + \
                        parsed_url.hostname + \
                        parsed_url.path + \
                        '/' + \
                        link
                        
                    self.links.append(temp)

                # Append link to the current url
                elif re.search('^(\.\/|[0-9a-zA-Z_-]+)', link):
                    temp = f'{parsed_url.scheme}://' + \
                        parsed_url.hostname + \
                        parsed_url.path.rsplit('/', maxsplit=1)[0] + \
                        '/' + \
                        link
                    
                    self.links.append(temp)

                # Append link to the target which contain protocol schema
                elif re.search('^\/', link):
                    temp = f'{parsed_url.scheme}://' + \
                        parsed_url.hostname + \
                        link

                    self.links.append(temp)


    def find_static_files(self):

        links = self.links.copy()

        exts  = 'css|js|xml|yml|json|txt|inc|cfg|conf|ini|log|'
        exts += 'sql|db|mdb|'
        exts += 'ico|png|jpg|jpeg|svg|gif|webp|'
        exts += 'pdf|doc|docx|ppt|pptx|xlsx|xls|csv|'
        exts += 'mp3|mp4|mkv|m4v|'
        exts += 'woff2|woff|ttf|'
        exts += 'zip|tar|gz|'
        exts += 'apk|exe|dmg|img|bin'
        exts += '|' + exts.upper()

        for link in links:
            if re.findall( f'\.({exts})', link ):
                self.static_files.append(link)
                self.links.remove(link)


    """
        Getter methods
    """
    def get_links(self):
        return self.links
    
    def get_static_files(self):
        return self.static_files

####### DEBUGGING ########
if __name__ == "__main__":
    if len(sys.argv) == 2:
        with open(sys.argv[1], 'r') as f:
            json_file = json.load(f)
        LinkParser(json_file)
    else:
        print(sys.argv)
        print(len(sys.argv))
        print("Usage: LinkParser.py <json-file>")
####### DEBUGGING ########
