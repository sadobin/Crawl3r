#! /usr/bin/python3 

from bs4 import BeautifulSoup, Comment
from config import HTML_ATTRIBUTES, HTML_TAGS
import re



class PageScraper:
    
    def __init__(self, page_content):

        self.comments = []
        self.links    = []
        self.tags     = {}

        self.bs = BeautifulSoup(page_content, 'html.parser')

        self.comments += self.bs.find_all(text=lambda it: isinstance(it, Comment))
        self.links    += self.find_links(page_content)

        for tag in HTML_TAGS:
            self.tags.update( self.find_tag(tag) )


    def find_links(self, page_content):
        """
            Find links from specified attributes
        """
        
        links = []

        page_content = str(page_content).split(' ')
        match_ptrn   = f"^{HTML_ATTRIBUTES}=(\"|').+(\"|')"
        remove_ptrn  = f"^{HTML_ATTRIBUTES}="

        for line in page_content:
            if re.match(match_ptrn, line):
                t = re.search(match_ptrn, line).group()
                t = re.sub(remove_ptrn, '', t)
                t = re.sub('(\'|")', '', t)
                links.append(t)

        return links


    def find_tag(self, tagname):
        """
            Find specified tags
        """
        tags = {}
        tags[tagname] = []

        for t in self.bs.find_all(tagname):
            # tags += dict(t.extract())
            tags[tagname].append(str(t))

        return tags


    # Getter methods
    def get_comments(self):
        return self.comments

    def get_links(self):
        return self.links

    def get_tags(self):
        return self.tags