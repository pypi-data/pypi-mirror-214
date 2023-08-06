# MySQL restore integrity check
Module can be used to test the database integrigity after restore the database. It will compare tables and show the only that tables in tabular format, Which had diffrencial records in after restore. 

## Requirements
- python3.6 or above
- tablular and os python plugin should be installed using pip3

## How to use
```
$ pip3 install databaseRestoreIntegrity
$ export SRC_DB_HOST='origin_database_hostname'
$ export SRC_DB_USER='origin_database_username'
$ export SRC_DB_PASS='origin_database_password'
$ export DST_DB_HOST='restored_database_hostname'
$ export DST_DB_USER='restored_database_username'
$ export DST_DB_PASS='restored_database_password'
```

### Now create and run a python scrip using the content below
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




