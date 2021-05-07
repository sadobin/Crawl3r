#! /usr/bin/python3

from collections import Counter
import re
import sys


class LinkParser:

    def __init__(self, reqer_result):

        try:
            self.links        = []
            self.all_paths    = []
            self.static_files = []
            self.reqer_result = reqer_result

            self.prepare_links()
            self.links = list( Counter(self.links).keys() )     # Put away duplicate links
            self.find_static_files()

            self.all_paths += self.links + self.static_files

        except Exception as e:
            print(f"[!] LinkParser: {e}")
            sys.exit(1)
    

    def prepare_links(self):

        """
            Prepare links for next crawl
        """

        schema_ptrn = '^http(s?):\/\/'

        for url in self.reqer_result:
            """
                target: protocol schema + hostname
                host: hostname
            """

            self.links.append(url)

            target = re.search(f'{schema_ptrn}([0-9a-zA-Z-]+\.)?[0-9a-zA-Z-]+\.[0-9a-zA-Z-]+', url).group()

            host = re.sub(f"{schema_ptrn}", '', target)
            host = re.search('[0-9a-zA-Z-]+\.[0-9a-zA-Z-]+$', host).group()


            for link in self.reqer_result[url]['links']:

                url  = url.split('?')[0]
                link = link.split('#')[0]

                # Ignore special protocols
                if re.search( '^(mailto:|tel:|javascript:|data:|android-app:|ios-app:|\{)', link ):
                    pass

                # Ignore domains which has different hostname (third-party domains)
                elif re.search( schema_ptrn, link ):
                    if re.search(f'{schema_ptrn}([0-9a-zA-Z-]+\.)?{host}(\/)?', link):
                        self.links.append( link )
                    else:
                        pass

                # if link starts with 'two forward slash' contain hostname, insert http at beginning of it then append.
                elif re.search( '^\/\/', link ) and re.search( f'^\/\/([0-9a-zA-Z-]+\.)?{host}(\/)?', link ):
                    temp = f"http:{link}"
                    self.links.append( temp )
                
                # Append link to the current url
                elif re.search('^(\?|\/\?)', link):
                    temp = url + link
                    self.links.append( temp )

                # Append link to the current url
                elif re.search('^\.\.', link):
                    temp  = url + f'/{link}'

                # Append link to the current url
                elif re.search('^\.\/', link):
                    path = url.split("?")[0]
                    parent_dir = path.rsplit("/", maxsplit=1)[0]
                    temp = parent_dir + link[1:]
                    self.links.append( temp )

                # Append link to the target which contain protocol schema
                elif re.search( '^([a-zA-Z0-9_-]|\/[a-zA-Z0-9_-])', link ):
                    temp  = target
                    temp += link if link.startswith('/') else f"/{link}"
                    self.links.append( temp )
        
        
 
    def find_static_files(self):

        links = self.links.copy()

        exts  = 'css|js|xml|yml|json|txt|inc|cfg|conf|ini|log|'
        exts += 'sql|db|mdb|'
        exts += 'ico|png|jpg|jpeg|svg|gif|'
        exts += 'pdf|doc|docx|ppt|pptx|xlsx|xls|csv|'
        exts += 'mp3|mp4|mkv|'
        exts += 'woff2|woff|'
        exts += 'zip|tar|gz'

        for link in links:
            if re.findall( f'\.({exts})', link ):
                self.static_files.append(link)
                self.links.remove(link)


    """
        Getter methods
    """

    def get_all_paths(self):
        return self.all_paths

    def get_links(self):
        return self.links
    
    def get_static_files(self):
        return self.static_files