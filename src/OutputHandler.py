#! /usr/bin/python3

import time
import datetime
import json
from collections import Counter
import os, sys
sys.path.append( os.path.dirname( os.path.dirname( os.path.realpath(__file__) ) ) )

import config


class OutputHandler:


    def __init__(self, hostname):
        self.hostname = hostname
        self.dir = config.RESULT_PATH
        self.date = datetime.datetime.fromtimestamp( time.time() ).strftime("%y-%m-%d")

        log_file = f'{self.dir}/logger.{self.hostname}.{self.date}.log'
        self.log_file = open(log_file, 'w')



    def logger(self, log):
        Time = datetime.datetime.fromtimestamp( time.time() ).strftime("%H:%M:%S")  # Return current time
        self.log_file.writelines(f"[ {Time} ] {log}\n")
        print(f"\33[36m[ {Time} ]\33[0m {log}")


    
    def final_result(self, redis_pool, been_crawled):

        self.redis_pool = redis_pool

        reqer_result = self.redis_fetcher('reqer_result')
        reqer_result = self.prettify_reqer_result(reqer_result)
        all_paths = self.redis_fetcher('all_paths')
        all_paths = list( Counter(all_paths).keys() )       # Make it unique
        static_files = self.redis_fetcher('static_files')
        static_files = list( Counter(static_files).keys() ) # Make it unique

        self.file_writer('reqer-result', reqer_result)
        self.file_writer('all-paths', all_paths)
        self.file_writer('static-files', static_files)
        self.file_writer('been-crawled', been_crawled)



    def file_writer(self, name, data):
        filename = f'{self.dir}/{name}.{self.hostname}.{self.date}.json'
        with open(filename, 'w') as f:
            data = json.JSONEncoder().encode(data)
            data = json.loads( data )
            json.dump( data, f, indent=4)



    def prettify_reqer_result(self, reqer_result):
        temp = {}
        for i in reqer_result:
            data = json.loads(i)
            temp.update(dict(data))
        
        return temp



    def redis_fetcher(self, name):
        temp = []
        for redis_client in self.redis_pool:
            temp += redis_client.lrange(name, 0, -1)
        
        return temp