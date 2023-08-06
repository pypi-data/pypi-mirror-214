# MySQL restore integrity check
Module can be used to test the database integrigity after restore the database. It will compare tables and show the only that tables in tabular format, Which had diffrencial records in after restore. 

## Requirements 
### MySQL
- python3.6 or above
- tablular and os python plugin should be installed using pip3

### PostgreSQL
- python3.6 or above
- tablular, os, Psycopg2 or Psycopg2-binary python plugin should be installed using pip3

### How to use MySQL
```
$ pip3 install databaseRestoreIntegrity
$ export SRC_DB_HOST='origin_database_hostname'
$ export SRC_DB_USER='origin_database_username'
$ export SRC_DB_PASS='origin_database_password'
$ export DST_DB_HOST='restored_database_hostname'
$ export DST_DB_USER='restored_database_username'
$ export DST_DB_PASS='restored_database_password'
```

### MySQL python script (Create and run on your local or from the host which can connect both db -- restored and active)
```
from databaseRestoreIntegrity import mysql
from tabulate import tabulate
import os

src_db_host = os.environ['SRC_DB_HOST']
src_db_pass = os.environ['SRC_DB_PASS']
src_db_user = os.environ['SRC_DB_USER']
dst_db_host = os.environ['DST_DB_HOST']
dst_db_pass = os.environ['DST_DB_PASS']
dst_db_user = os.environ['DST_DB_USER']



restored_db = mysql.mysqlReadData(dst_db_host, dst_db_user, dst_db_pass)
active_db = mysql.mysqlReadData(src_db_host, src_db_user, src_db_pass)

restored_db._create_tmp_file('restored_db')
active_db._create_tmp_file('active_db')
restored_db._insert_data('restored_db')
restored_db._insert_data('active_db')


def check_consistency():
    unconsistent_tabels = []
    conn = restored_db.connection()
    check_consistency = conn.cursor()
    check_consistency.execute("USE CheckDBsTableConsistency")
    check_consistency.execute("select tables_name, records_count, hostname from (select tables_name, hostname, records_count from active_db union all select tables_name, hostname, records_count from restored_db) temp group by tables_name, records_count having count(*) = 1")
    result = check_consistency.fetchall()
    print(tabulate(result, headers=['tables_name', 'records_count'], tablefmt='psql'))
    conn.close()
check_consistency()
```

### How to use PostgreSQL
```
$ pip3 install databaseRestoreIntegrity
$ export SRC_DB_HOST='origin_database_hostname'
$ export SRC_DB_USER='origin_database_username'
$ export SRC_DB_PASS='origin_database_password'
$ export DST_DB_HOST='restored_database_hostname'
$ export DST_DB_USER='restored_database_username'
$ export DST_DB_PASS='restored_database_password'
$ export DB_NAME='database_name' 
```

**Note:** Postgres need databsebase name to connectivity


### PostgreSQL python script (Create and run on your local or from the host which can connect both db -- restored and active)
```
from databaseRestoreIntegrity import postgres
from tabulate import tabulate
import os

src_db_host = os.environ['SRC_DB_HOST']
src_db_pass = os.environ['SRC_DB_PASS']
src_db_user = os.environ['SRC_DB_USER']
dst_db_host = os.environ['DST_DB_HOST']
dst_db_pass = os.environ['DST_DB_PASS']
dst_db_user = os.environ['DST_DB_USER']
db_name = os.environ['DB_NAME']



restored_db = postgres.pgsqlReadData(dst_db_host, dst_db_user, dst_db_pass, db_name)
active_db = postgres.pgsqlReadData(src_db_host, src_db_user, src_db_pass, db_name)

restored_db._create_tmp_file('restored_db')
active_db._create_tmp_file('active_db')
restored_db._insert_data('restored_db')
restored_db._insert_data('active_db')


def check_consistency():
    unconsistent_tabels = []
    sql_query = "SELECT COALESCE(s.tables_name,t.tables_name) id, \
                s.records_count records_count, t.records_count records_count, \
                CASE WHEN s.records_count = t.records_count THEN 'equal' \
                    WHEN s.tables_name IS NULL THEN 'Table not on source' \
                    WHEN t.tables_name IS NULL THEN 'Table not on target' \
                    ELSE 'difference' \
                END compare_result \
                FROM CheckDBsTableConsistency.active_db s \
                FULL JOIN CheckDBsTableConsistency.restored_db t ON s.tables_name=t.tables_name"
    conn = restored_db.connection()
    check_consistency = conn.cursor()
    check_consistency.execute(sql_query)
    result = check_consistency.fetchall()
    print(tabulate(result, headers=['tables_name', 'records_count_active_db', 'records_count_restored_db', 'compare_result'], tablefmt='psql'))
    conn.close()
check_consistency()
```






