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

    def __init__(self, target, CRAWLER_DIR, PG_HOST, PG_PORT):

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

        if os.environ['PG_USER'] and os.environ['PG_PASS']:
            self.pg_global_pool = PostgresqlConnection(
                pg_host=PG_HOST,
                pg_port=PG_PORT,
                pg_user=os.environ['PG_USER'],
                pg_pass=os.environ['PG_PASS'],
                target=self.hostname,
                CRAWLER_DIR = CRAWLER_DIR
            )

        self.output_handler = OutputHandler(self.hostname,CRAWLER_DIR)
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



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Crawl3r: A tool for web crawling")
    parser.add_argument('-u', '--url', dest='target', help='Specify the target url', required=True)
    parser.add_argument('-BD', '--BaseDirectory', dest='base_directory', help='Specify the base directory', required=True)
    parser.add_argument('--pghost', dest='p_host', help='Specify the PostgreSQL server (default: localhost)')
    parser.add_argument('--pgport', dest='p_port', help='Specify the PostgreSQL port (default: 5432)')
    parser.add_argument('-UA', '--useragent', dest='user_agent', help='Specify the User-Agent')
    parser.add_argument('-H', '--Header', dest='header', help='Specify custom headers')
    parser.add_argument('-C', '--Cookie', dest='cookie', help='Specify cookies')

    args = parser.parse_args()

    try:
        TARGET = args.target
        CRAWLER_DIR = args.base_directory
        PG_HOST = "localhost"
        PG_PORT = "5432"

        if args.p_host:
            PG_HOST = args.p_host
        if args.p_port:
            PG_HOST = args.p_port
        crawpy = Crawl3r(TARGET, CRAWLER_DIR, PG_HOST, PG_PORT)

    except Exception as e:
        print(f"\33[31m[!]\33[0m Crawl3r: {e}")