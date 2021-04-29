#! /usr/bin/python3

import redis
import sys



class RedisConnection:

    def __init__(self, host='localhost', port=6379, instances=1):

        self.redis_pool = []

        self.host = host
        self.port = port
        self.dbs  = list( range(1, instances+1) )

        self.connection()
        info = '\33[33m[.]\33[0m'
        print(f"{info} Initialize {instances} redis client(s).")


    def connection(self):

        for db in self.dbs:
            try:
                redis_client = redis.Redis(
                    host=self.host, 
                    port=self.port, 
                    db=db, 
                    decode_responses=True)

                redis_client.flushall()
                self.redis_pool.append( redis_client )
            
            except Exception as e:
                alert = "\33[31m[!]\33[0m"
                print(f"{alert} RedisConnection: {e}")
                sys.exit(1)


    def get_redis_pool(self):
        return self.redis_pool