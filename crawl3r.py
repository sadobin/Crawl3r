#! /usr/bin/python3 

from multiprocessing import Process, Manager
from urllib.parse import urlparse
from collections import Counter
import sys, argparse, os
import json
import numpy as np

from src.Reqer import Reqer
from src.LinkParser import LinkParser
from src.RedisConnection import RedisConnection
from src.PostgresqlConnection import PostgresqlConnection
from src.OutputHandler import OutputHandler
import config



class Crawl3r:

    def __init__(self, target):

        sys.setrecursionlimit(100000)
        os.system("ulimit -n 8192")  # Increase user limitation

        if target.startswith("http"):
            self.hostname = urlparse(target).hostname
        else:
            self.hostname = target.split('/')[0]
        self.reqer_result = {}
        # Links to crawl
        self.links = np.array([])
        # New links to crawl
        self.new_links = []
        # Founded static files
        self.static_files = []
        # Crawled paths
        self.been_crawled = np.array([])

        self.links = np.append(self.links, target)

        self.pg_global_pool = PostgresqlConnection(
                target=self.hostname,
                pg_user=os.environ['PG_USER'],
                pg_pass=os.environ['PG_PASS'],
                pg_host=config.PG_HOST,
                pg_port=config.PG_PORT,
            )
        
        self.output_handler = OutputHandler(self.hostname)
        self.process_generator()

    def process_generator(self):

        count = 0
        try:

            while True:

                # Remove links that has been crawled
                self.links = np.unique(self.links).tolist()
                self.links = list(filter(lambda x: x not in self.been_crawled.tolist(), self.links))

                if len(self.links):
                    """
                        Split total links to groups of <n> links.
                        Numerical example: (groups of 5 links)

                            links: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
                            link_groups: [[0, 1, 2, 3, 4], [5, 6, 7, 8, 9], [10, 11, 12]]
                    """
                    n = config.PROCESSES
                    link_groups = [self.links[i:i + n] for i in range(0, len(self.links), n)]

                    for links in link_groups:
                        procs = []
                        # handle return values of the reqer_process method
                        manager = Manager()
                        return_links = manager.list()
                        for link in links:
                            p = Process(
                                target=self.reqer_process,
                                args=(link, return_links)
                            )
                            procs.append(p)
                            self.output_handler.logger(f"CRAWLING {link}")
                            p.start()
                        for proc in procs: proc.join()
                        self.new_links += return_links

                    count += 1

                else:
                    green = "\33[32m[*]\33[0m"
                    print(f"{green} CRAWLING FINISHED")
                    break

                # Update self.been_crawled and get new links from redis_clients
                self.links_handler()

                if count == config.DEPTH:
                    break

        except KeyboardInterrupt:
            print(f"\33[31m[!]\33[0m Keyboard Interrupt")
            # Write final results
            self.output_handler.logger('Saving result')
            self.output_handler.final_result(self.pg_global_pool, self.been_crawled.tolist())
            sys.exit(1)

        # Write current result to the file
        self.output_handler.logger('Saving result')
        self.output_handler.final_result(self.pg_global_pool, self.been_crawled.tolist())

    def reqer_process(self, target, return_links):

        reqer = Reqer(target)
        reqer_result = reqer.get_result()

        link_parser = LinkParser(reqer_result)

        je = json.JSONEncoder()
        reqer_result = je.encode(reqer_result)
        links = list(filter(lambda x: x not in self.been_crawled.tolist(), link_parser.get_links()))
        static_files = link_parser.get_static_files()

        self.pg_global_pool.insert_data('reqer_result', reqer_result) if len(reqer_result) else None
        self.pg_global_pool.insert_data('static_files', static_files) if len(static_files) else None

        # self.new_links += links if len(links) else None
        if len(links): return_links += links


    def links_handler(self):
        # self.been_crawled += self.links
        self.been_crawled = np.append(self.been_crawled, self.links)
        self.links = self.new_links.copy()


def cmd_arguments():
    parser = argparse.ArgumentParser(description="Crawl3r Help")
    
    ### Base Configuration
    base_config = parser.add_argument_group("Base Configuration")
    base_config.add_argument('target', help='Specify the target url')
    base_config.add_argument('-cd', '--crawler-dir', dest='crawler_dir', help='Specify the base directory')
    base_config.add_argument('--pghost', help='Specify the PostgreSQL server (default: localhost)')
    base_config.add_argument('--pgport', help='Specify the PostgreSQL port (default: 5432)', type=int)
    
    ### Configuration
    configs = parser.add_argument_group("Configuration")
    configs.add_argument('-d', '--depth', help='Depth of crawling')
    configs.add_argument('-js', '--parse-js', help='Parse javascript during runtime', action="store_true")
    # Implement to accept regex
    configs.add_argument('-p', '--process', help='Number of process for multiprocessing (default: 8)', type=int)
    # TODO: add random user-aget value
    configs.add_argument('-ua', '--useragent', type=str ,help='Specify the User-Agent (fu, fd, ff, fc, f7, f10, fan, fm, fi, cu, cf, ca, can, cm, ci, e7, e10, ean, em, ei): check the UserAgentParser.py')
    # TODO: implement list user agent function
    configs.add_argument('-H', '--header', help='Specify custom headers: Authorization, Cookie, etc')
    configs.add_argument('-a', '--attrs', help='Custom HTML attributes (in regex formats) to looking for links (default: (href|src|action))')
    
    ### Modules
    modules = parser.add_argument_group("Modules")
    modules.add_argument('-m', '--module', help='Available modules: ps (PageScraper), dbf (database fetcher)')
    configs.add_argument('-t', '--tags', help='Specified tags for PageScraper module')
    modules.add_argument('-r', '--resume', help='Resume the crawling from where the crawl3r stopped (been_crawled.json file is required)')

    ### Scope
    scope = parser.add_argument_group("Scope Configuration")
    scope.add_argument('-s', '--subdomains', help='weather crawl the subdomains or not')
    scope.add_argument('-e', '--exclude-path', help='Exclude specified paths for crawling (e.g. sensitive paths like admin dashboard)')

    ### List Features
    list_features = parser.add_argument_group("List Features")
    list_features.add_argument('-lu', '--list-ua', help='List availabe user-agents', action="store_true")
    list_features.add_argument('-lm', '--list-modules', help='List availabe modules', action="store_true")

    args = parser.parse_args()


    # Edit config.py for defined arguments
    opts = {
        'crawler_dir': 'CRAWLER_DIR',
        'pghost': 'PG_HOST',
        'pgport': 'PG_PORT',
        'process': 'PROCESSES',
        'depth': 'DEPTH',
        'useragent': '',
        'header': 'REQUEST_HEADERS',
        'attrs': 'HTML_ATTRIBUTES',
        'exclude_path': 'EXCLUDED_PATH',
        'tags': 'HTML_TAGS',
    }
    for cmd_arg, config_opt in opts.items():
        if 'header' in cmd_arg:
            name, value = args.header.split(':', maxsplit=1)
            config.REQUEST_HEADERS.update( {name.strip(): value.strip()} )
        if 'useragent' in cmd_arg:
            config.REQUEST_HEADERS.update( {'User-Agent': getattr(args, cmd_arg)} )
        else:
            setattr(config, config_opt, getattr(args, cmd_arg))
        
        print(f'[===] {cmd_arg}: {getattr(args, cmd_arg)}')

    return args.target


def check_envs():
    envs_list = ['PG_USER', 'PG_PASS']
    for env in envs_list:
        if not os.environ.get(env): raise Exception(f"The {env} value not defined")
        setattr(config, env, os.environ.get(env))


def main():
    check_envs()
    target = cmd_arguments()
    try:
        crawpy = Crawl3r(target)
    except Exception as e:
        print(f"\33[31m[!]\33[0m Crawl3r: {e}")



if __name__ == "__main__": main()