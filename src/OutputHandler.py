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

    def __init__(self, hostname, date=None, target_dir=""):
        self.hostname = hostname
        self.dir = self.create_target_dir(hostname, date=date, target_dir=target_dir)
        # date = datetime.datetime.fromtimestamp(time.time()).strftime("%y-%m-%d")
        date = datetime.now().strftime("%y.%m.%d")
        
        log_file = f'{self.dir}/logger.{self.hostname}.{date}.log'
        self.log_file = open(log_file, 'w+') if not target_dir else ''

    # TODO: create various log level
    def logger(self, log):
        time_ = datetime.now().strftime("%y.%m.%d-%H.%M.%S")  # Return current time
        self.log_file.writelines(f"[ {time_} ] {log}\n")
        print(f"\33[36m[ {time_} ]\33[0m {log}")


    def final_result(self, pg_global_pool, been_crawled=None):
        conn = pg_global_pool.create_connection()
        reqer_result = pg_global_pool.fetch_data(conn, 'reqer_result')
        
        conn = pg_global_pool.create_connection()
        static_files = pg_global_pool.fetch_data(conn, 'static_files')

        conn = pg_global_pool.create_connection()
        been_crawled = pg_global_pool.fetch_data(conn, 'been_crawled') if not been_crawled else been_crawled
        all_paths = list(Counter(been_crawled + static_files).keys())

        self.file_writer('reqer-result', reqer_result)
        self.file_writer('all-paths', all_paths)
        self.file_writer('static-files', static_files)
        self.file_writer('been-crawled', been_crawled)


    def create_target_dir(self, hostname, date, target_dir=''):
        """
            Path to save the result
        """
        now_time = datetime.now().strftime('%Y.%m.%d-%H.%M') if not date else date
        # home_dir = subprocess.check_output('echo $HOME', shell=True).decode().strip()
        if not config.CRAWLER_DIR:
            print('[!] Set the CRAWLER_DIR in config.py')
            sys.exit(1)
        
        result_dir = ""
        if not len(target_dir):
            result_dir = f"{config.CRAWLER_DIR}/{hostname}_{now_time}"
            if not os.path.exists(result_dir):
                os.mkdir(result_dir)
                logging.info(f'The result directory created ({result_dir})')
        else:
            result_dir = f"{config.CRAWLER_DIR}/{target_dir}"
            
        return result_dir


    def file_writer(self, name, data):
        time_ = datetime.now().strftime("%y.%m.%d-%H.%M.%S")  # Return current time
        filename = f'{self.dir}/{name}.{self.hostname}.{time_}.json'
        with open(filename, 'w') as f:
            data = json.JSONEncoder().encode(data)
            data = json.loads(data)
            json.dump(data, f, indent=4)
        logging.info(f"{name} saved into {filename}")

    @staticmethod
    def file_reader(filename):
        ## TODO: refactor file existence check in future
        if not os.path.exists(filename):
            raise Exception(f'[!] File {filename} not found')
        ##
        
        with open(filename, 'r') as f:
            content = f.read()
            return content


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
