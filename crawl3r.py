#! /usr/bin/python3 

from multiprocessing import Process
from urllib.parse import urlparse
from collections import Counter
import sys, os
import json


from src.Reqer import Reqer
from src.LinkParser import LinkParser
from src.RedisConnection import RedisConnection
from src.PostgresqlConnection import PostgresqlConnection
from src.OutputHandler import OutputHandler
import config



class Crawl3r:

    def __init__(self, target):

        sys.setrecursionlimit(100000)
        os.system("ulimit -n 8192")     # Increase user limitation

        if target.startswith("http"):
            self.hostname = urlparse(target).hostname
        else:
            self.hostname = target.split('/')[0]
        self.reqer_result = {}
        # Links to crawl
        self.links = []
        # Founded static files
        self.static_files = []
        # Crawled paths
        self.been_crawled = []
        # All paths founded
        self.all_paths = []

        self.links.append(target)

        if os.environ.get("REDIS_HOST"):
            self.redis_pool = RedisConnection(
                host=os.environ.get("REDIS_HOST"),
                instances=1).get_redis_pool()
        else:
            self.redis_pool = RedisConnection(instances=config.PROCESSES).get_redis_pool()

        if os.environ['PG_USER'] and os.environ['PG_PASS']:
            self.pg_global_pool = PostgresqlConnection(
                pg_user=os.environ['PG_USER'],
                pg_pass=os.environ['PG_PASS'],
                target=self.hostname
            )

        self.output_handler = OutputHandler(self.hostname)
        self.process_generator()


    def process_generator(self):

        count = 0

        try:

            while True:

                # Remove links that has been crawled
                self.links = list(Counter(self.links).keys())
                self.links = list( filter(lambda x: x not in self.been_crawled, self.links) )
                ############
                # pg_pool = self.pg_global_pool.get_pg_pool(config.PROCESSES)

                if len(self.links):
                    """
                        Split total links to groups of <n> links.
                        Numerical example: (groups of 5 links)

                            links: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
                            link_groups: [[0, 1, 2, 3, 4], [5, 6, 7, 8, 9], [10, 11, 12]]
                    """
                    n = config.PROCESSES
                    link_groups = [ self.links[i:i+n] for i in range(0, len(self.links), n) ]

                    for links in link_groups:

                        procs = []

                        # for link, redis_client in zip(links, self.redis_pool):
                        # for link, pg_conn in zip(links, pg_pool):
                        for link in links:
                            p = Process(
                                target=self.reqer_process, 
                                # args=(link, pg_conn)
                                args=(link,)
                                )
                            procs.append(p)

                            self.output_handler.logger(f"CRAWLING {link}")
                            p.start()

                        for proc in procs:
                            proc.join()

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
            self.output_handler.final_result(self.pg_global_pool, self.been_crawled)
            sys.exit(1)

        # Write current result to the file
        self.output_handler.logger('Saving result')
        self.output_handler.final_result(self.pg_global_pool, self.been_crawled)


    # def reqer_process(self, target, pg_conn):
    def reqer_process(self, target):

        reqer = Reqer(target)
        reqer_result = reqer.get_result()

        link_parser = LinkParser(reqer_result)

        je = json.JSONEncoder()

        reqer_result = je.encode(reqer_result)
        links = list( filter(lambda x: x not in self.been_crawled, link_parser.get_links()) )
        static_files = link_parser.get_static_files()
        all_paths = link_parser.get_all_paths()

        
        self.pg_global_pool.insert_data('reqer_result', reqer_result) if len(reqer_result) else None
        # self.pg_thread_pool.insert_data(pg_conn, 'links', links) if len(links) else None
        self.pg_global_pool.insert_data('static_files', static_files) if len(static_files) else None
        self.pg_global_pool.insert_data('all_paths', all_paths) if len(all_paths) else None

        ################################
        # self.pg_thread_pool.putaway_pg_conn(pg_conn)

        # redis_client.rpush('reqer_result', reqer_result) if len(reqer_result) else None
        self.redis_pool[0].rpush('links', *links) if len(links) else None
        # redis_client.rpush('static_files', *static_files) if len(static_files) else None
        # redis_client.rpush('all_paths', *all_paths) if len(all_paths) else None


    def links_handler(self):
        self.been_crawled += self.links
        self.links = []
        for redis_client in self.redis_pool:
            self.links += redis_client.lrange('links', 0, -1)



try:
    if len(sys.argv) == 2:
        target = sys.argv[1]
        crawpy = Crawl3r(target)
except Exception as e:
    print(f"\33[31m[!]\33[0m Crawl3r: {e}")
