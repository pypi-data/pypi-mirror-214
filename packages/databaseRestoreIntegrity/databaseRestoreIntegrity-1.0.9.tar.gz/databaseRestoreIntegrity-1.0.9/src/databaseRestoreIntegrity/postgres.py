#!/usr/bin/env python3

import psycopg2
import re
import os

class pgsqlReadData:

    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
    def connection(self):
        try:
            mydb = psycopg2.connect(
                host = self.host,
                user = self.user,
                password = self.password,
                database = self.database
        )   
        except:
            print(f'Connection is not successful')
        return mydb
    
    def _get_tables_raw_data(self):
        raw_tables_data = []
        # sql_query = "\dt *.*"
        conn = self.connection()
        mycursor = conn.cursor()
        mycursor.execute("SELECT schemaname,tablename FROM pg_catalog.pg_tables WHERE schemaname != 'pg_catalog' AND schemaname != 'information_schema'")
        for x in mycursor:
            raw_tables_data.append(str("{}.{}".format(*x)))
        return raw_tables_data

    
    def _get_count(self):
        records_count = []
        raw_tables = self._get_tables_raw_data()
        try:
            conn = self.connection()
            for x in raw_tables:   
                sql_query = ("{} {}".format("SELECT COUNT(*) FROM", x))
                mycursor = conn.cursor()
                mycursor.execute(sql_query)
                for c in mycursor:
                    records_count.append("{},{}".format(x, *c))
        except:
            print(f'database list not succedd')
        return records_count

    def _create_tmp_file(self, name):
        self.name = name
        records = self._get_count()
        f = open(self.name, 'w+')
        for data in records:
            sql_query = ("{}{}.{}{}{}".format('INSERT INTO ', 'CheckDBsTableConsistency', self.name, ' (tables_name, records_count, hostname) VALUES ', (data.split(",")[0], data.split(",")[1], self.host)))
            f.write("{}\n".format(sql_query))
        f.close()
    
    def _insert_data(self, name):
        conn = self.connection()
        self.name = name
        ct = conn.cursor()
        drop_table_sql = ("{} {}.{}".format('DROP TABLE IF EXISTS', 'CheckDBsTableConsistency', self.name))
        ct.execute('CREATE SCHEMA IF NOT EXISTS CheckDBsTableConsistency')
        ct.execute(drop_table_sql)
        ct.execute("{}{}.{}{}".format('CREATE TABLE IF NOT EXISTS ', 'CheckDBsTableConsistency', self.name, ' (tables_name VARCHAR(255) PRIMARY KEY, records_count VARCHAR(255), hostname VARCHAR(244))'))
        f = open(self.name, 'r')
        lines = f.readlines()
        count = 0
        for line in lines:
            count += 1
            sql_query = ("{}".format(line.strip()))
            ct.execute(sql_query)
            conn.commit()
        f.close()
        os.remove(self.name)
        conn.close()






        
   