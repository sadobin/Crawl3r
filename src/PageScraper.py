#! /usr/bin/python3 

import os, sys
sys.path.append( os.path.dirname( os.path.dirname( os.path.realpath(__file__) ) ) )

from bs4 import BeautifulSoup, Comment
from config import HTML_ATTRIBUTES, HTML_TAGS
import re
import json
from urllib.parse import urlparse
import subprocess


class PageScraper:
    
    def __init__(self, page_content=None, reqer_result=None, reqer_result_path=None):

        self.links    = []
        if page_content:
            self.links += self.find_links(page_content)        
        elif reqer_result:
            self.page_scraper_wrapper(reqer_result, reqer_result_path)


    def page_scraper_wrapper(self, reqer_result, reqer_result_path):
        comments = []
        tags = {}
        result = {}
        output_dir = reqer_result_path.rsplit('/', maxsplit=1)[0]
        reqer_result = json.loads(reqer_result)

        for url in reqer_result:
            temp = {}
            print(url)
            bs = BeautifulSoup(reqer_result[url]['response'], 'html.parser')
            
            # if len(bs.contents) == 2:
            self.file_structure(output_dir, url, str(bs.contents))
            
            comments += bs.find_all(text=lambda it: isinstance(it, Comment))
            temp.update( {'comments': comments} )
            
            for tag in HTML_TAGS:
                if tag:
                    tags.update(self.find_tag(bs, tag))
            
            temp.update( {'tags': tags} )

            result.update( {url: temp} )
        
        # print(json.dumps(result, indent=4))


    def file_structure(self, path, url, content):
        base_path = f"{path}/file-structure"
        file_dir = ""
        file_path = ""
        file_name = ""
        
        parsed_url = urlparse(url)
        # url_path = parsed_url.path.rsplit('/', maxsplit=1)[-1]
        url_path = parsed_url.path
        url_path = url_path[:-1] if url_path.endswith('/') else url_path        

        if '.' in url_path.rsplit('/', maxsplit=1)[-1]:  # file has extension
            file_dir = url_path.rsplit('/', maxsplit=1)[0]
            file_name = url_path.rsplit('/', maxsplit=1)[-1]
        else:
            file_dir = url_path
            file_name = file_dir.rsplit('/', maxsplit=1)[-1] + '.html'

        file_dir  = base_path + '/' + file_dir
        file_dir = file_dir.replace('//', '/')
        file_path = file_dir + '/' + file_name
        file_path +=  f'?{parsed_url.query}' if parsed_url.query else ''

        print(f'-- {file_dir}')
        print(f'-- {file_path}')

        mkdir_cmd = f""" mkdir -p "{file_dir}" """
        touch_cmd = f""" touch  "{file_path}" """
        subprocess.run(mkdir_cmd, shell=True)
        # os.makedirs(file_dir, exist_ok=True)
        subprocess.run(touch_cmd, shell=True)

        with open(file_path, 'w') as f:
            f.write(content)



    def find_links(self, page_content):
        """
            Find links from specified attributes
        """
        
        links = []

        page_content = str(page_content).replace('>', '> ')
        page_content = page_content.split(' ')
        match_ptrn   = f"^{HTML_ATTRIBUTES}=(\"|').+(\"|')"
        remove_ptrn  = f"^{HTML_ATTRIBUTES}="

        for line in page_content:
            if re.match(match_ptrn, line):
                t = re.search(match_ptrn, line).group()
                t = re.sub(remove_ptrn, '', t)
                t = re.sub('(\'|")', '', t)
                links.append(t)

        return links


    def find_tag(self, beautiful_soup, tagname):
        """
            Find specified tags
        """
        tags = {}
        tags[tagname] = []

        for t in beautiful_soup.find_all(tagname):
            tags[tagname].append(str(t))

        return tags


    """
        Getter methods
    """
    def get_comments(self):
        return self.comments

    def get_links(self):
        return self.links

    def get_tags(self):
        return self.tags