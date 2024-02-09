#! /usr/bin/python3
import logging
import os
import sys
from datetime import datetime
import copy
from collections import Counter


import psycopg2
from psycopg2 import pool


sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from OutputHandler import OutputHandler
import config




class PostgresqlConnection:

    def __init__(self, pg_user, pg_pass, target, host='localhost', port=5432):
        self.output_handler = OutputHandler(target)

        now_time = datetime.now().strftime('%Y.%m.%d-%H.%M')
        self.db_name = f'crawler_{target}_{now_time}'
        self.pg_dsn = {
            'database': self.db_name,
            'user': pg_user,
            'password': pg_pass,
            'host': host,
            'port': port,
        }

        # Creating crawler database
        self.create_db(self.db_name, pg_user)

        # self.pg_global_conn = psycopg2.connect(
        #     user=pg_user,
        #     password=pg_pass,
        #     host=host,
        #     port=port,
        #     database=self.db_name,
        #     # async_=True
        # )

        # self.pg_pool = psycopg2.pool.ThreadedConnectionPool(
        #     minconn=config.PROCESSES,
        #     maxconn=config.PROCESSES,
        #     user=pg_user,
        #     password=pg_pass,
        #     host=host,
        #     port=port,
        #     database=self.db_name,
        #     # async_=True
        # )

        # self.pg_pool = asyncpg.create_pool(
        #     user=pg_user,
        #     password=pg_pass,
        #     host=host,
        #     port=port,
        #     database=self.db_name,
        #     min_size=config.PROCESSES,
        #     max_size=config.PROCESSES
        # )

        conn = self.create_connection(**self.pg_dsn)
        self.create_tables(conn)
        conn.close()
        # self.pg_global_conn.putconn(conn)


    def create_connection(self, **kwargs):
        dsn = copy.deepcopy(self.pg_dsn)
        
        expected_values = ['user', 'password', 'host', 'port', 'database']
        for value in expected_values:
            if value in kwargs.keys():
                dsn.update({value: kwargs.get(value)})
        
        return psycopg2.connect(**dsn)


    def create_db(self, db_name, pg_user):
        dsn = copy.deepcopy(self.pg_dsn)
        dsn.update({'database': 'postgres'})
        conn = self.create_connection(**dsn)

        conn.autocommit = True
        cursor = conn.cursor()

        try:
            # Create target database
            create_db_query = f'CREATE DATABASE "{db_name}" ENCODING "UTF8" OWNER {pg_user}'
            cursor.execute(create_db_query)
            conn.commit()
            self.output_handler.logger(f'POSTGRESQL: database {db_name} created')
        except Exception as e:
            conn.rollback()
            self.output_handler.logger(f'ERROR: {e}')
            sys.exit(1)
        finally:
            # Close the cursor and connection
            cursor.close()
            conn.close()



    def create_tables(self, conn):
        # Create target tables
        tables_query = {
            # "reqer_result": "CREATE TABLE reqer (status integer, req_headers json, res_headers json, res text, extras json);",
            "reqer_result": "CREATE TABLE reqer_result (result json);",
            "static_files": "CREATE TABLE static_files (links text[]);",
            # "all_paths": "CREATE TABLE all_paths (links text[]);",
            "been_crawled": "CREATE TABLE been_crawled (links text[]);",
        }
        conn.autocommit = True
        cursor = conn.cursor()

        try:
            # Create target database
            for tbl_name, query in tables_query.items():
                cursor.execute(query)
                conn.commit()
                # conn.execute(query)
                self.output_handler.logger(f'POSTGRESQL: table {tbl_name} created')
        except Exception as e:
            conn.rollback()
            self.output_handler.logger(f'ERROR: {e}')
        finally:
            # Close the cursor and connection
            cursor.close()
            conn.close()

    # TODO
    def fetch_data(self, conn, table):
        fetch_query = {
            # "reqer_result": f"INSERT INTO reqer_result (status, req_headers, res_headers, res, extras) VALUES (%d,%s,%s,%s,%s);",
            "reqer_result": "SELECT * FROM reqer_result;",
            "static_files": "SELECT * FROM static_files;",
            # "all_paths": "SELECT * FROM all_paths;",
            "been_crawled": "SELECT * FROM been_crawled;",
        }

        query = fetch_query.get(table)
        cursor = conn.cursor()
        cursor.execute(query)
        res = cursor.fetchall()

        if table == 'reqer_result':
            r = {}
            for l in res:   r.update(dict(l[0]))
            return r
        else:
            r = []
            for l in res:   r += list(l)[0]
            r = list(Counter(r).keys())
            return r
            




    def insert_data(self, table, data):

        insert_query = {
            # "reqer_result": f"INSERT INTO reqer_result (status, req_headers, res_headers, res, extras) VALUES (%d,%s,%s,%s,%s);",
            "reqer_result": "INSERT INTO reqer_result (result) VALUES (%s);",
            "static_files": "INSERT INTO static_files (links) VALUES (%s);",
            # "all_paths": "INSERT INTO all_paths (links) VALUES (%s);",
            "been_crawled": "INSERT INTO been_crawled (links) VALUES (%s);",
        }
        query = insert_query.get(table)
        
        """
        if   table == "reqer_result":
            query = insert_query.get(table).format(data)
            # query = insert_query.get(table).format(
            #     int(data['status-code']),
            #     data['request-headers'],
            #     data['response-headers'],
            #     data['response'],
            #     data['extra'],
            # )
        elif table == "static_files":
            query = insert_query.get(table).format(data)
        elif table == "been_crawled":
            query = insert_query.get(table).format(data)
        """

        conn = self.create_connection(**self.pg_dsn)
        conn.autocommit = True
        cursor = conn.cursor()
        try:
            cursor.execute(query, (data,))
            # Commit the changes
            conn.commit()
            # self.output_handler.logger("Data inserted successfully.")
        except Exception as e:
            # Rollback the changes in case of an error
            conn.rollback()
            logging.info("------------")
            logging.info(f"TABLE: {table}")
            # logging.info(f"DATA: {data}")
            logging.info(f"QUERY: {query}")
            logging.error(f"Error inserting data: {e}")
        finally:
            # Close the cursor and connection
            cursor.close()
            conn.close()


    def get_pg_pool(self, count):
        # pool = [self.pg_global_conn.getconn() for i in range(count)]
        pool = [self.create_connection(**self.pg_dsn) for i in range(count)]
        return pool


    def putaway_pg_conn(self, conn):
        self.pg_global_conn.putconn(conn)





if __name__ == "__main__":
    try:
        pg_user = os.environ['PG_USER']
        pg_pass = os.environ['PG_PASS']
    except Exception as e:
        logging.error('The PG_USER and PG_PASS does not provided')

    if pg_user and pg_pass:
        pg_conn = PostgresqlConnection(pg_user, pg_pass, target='asus.com')
