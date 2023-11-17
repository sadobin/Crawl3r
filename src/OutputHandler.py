#! /usr/bin/python3

import time
from datetime import datetime
import json
from collections import Counter
import os
import sys
import subprocess
import logging
import config

logging.basicConfig(level=logging.INFO)
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))


class OutputHandler:

    def __init__(self, hostname):
        self.hostname = hostname
        self.dir = self.create_target_dir(hostname)
        # date = datetime.datetime.fromtimestamp(time.time()).strftime("%y-%m-%d")
        date = datetime.now().strftime("%y-%m-%d")
        
        log_file = f'{self.dir}/logger.{self.hostname}.{date}.log'
        self.log_file = open(log_file, 'w+')

    def logger(self, log):
        # time_ = datetime.datetime.fromtimestamp(time.time()).strftime("%H-%M-%S")  # Return current time
        time_ = datetime.now().strftime("%H-%M-%S")  # Return current time
        self.log_file.writelines(f"[ {time_} ] {log}\n")
        print(f"\33[36m[ {time_} ]\33[0m {log}")


    def final_result(self, pg_global_pool, been_crawled):
        # self.redis_pool = redis_pool
        # reqer_result = self.redis_fetcher('reqer_result')
        # reqer_result = self.prettify_reqer_result(reqer_result)
        # all_paths = self.redis_fetcher('all_paths')
        # all_paths = list(Counter(all_paths).keys())  # Make it unique
        # static_files = self.redis_fetcher('static_files')
        # static_files = list(Counter(static_files).keys())  # Make it unique

        conn = pg_global_pool.create_connection()
        reqer_result = ''
        all_paths = ''
        static_files = ''

        self.file_writer('reqer-result', reqer_result)
        self.file_writer('all-paths', all_paths)
        self.file_writer('static-files', static_files)
        self.file_writer('been-crawled', been_crawled)


    def create_target_dir(self, hostname):
        """
            Path to save the result
        """
        now_time = datetime.now().strftime('%Y-%m-%d.%H-%M')
        home_dir = subprocess.check_output('echo $HOME', shell=True).decode().strip()
        if not config.CRAWLER_DIR:
            print('[!] Set the CRAWLER_DIR in config.py')
            sys.exit(1)
        result_dir = f"{config.CRAWLER_DIR}/{hostname}.{now_time}"
        if not os.path.exists(result_dir):
            os.mkdir(result_dir)
            logging.info(f'The result directory created ({result_dir})')
        return result_dir


    def file_writer(self, name, data):
        time_ = datetime.now().strftime("%H-%M-%S")  # Return current time
        filename = f'{self.dir}/{name}.{self.hostname}.{time_}.json'
        with open(filename, 'w') as f:
            data = json.JSONEncoder().encode(data)
            data = json.loads(data)
            json.dump(data, f, indent=4)


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
