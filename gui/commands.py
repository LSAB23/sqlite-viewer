import sqlite3

get_tables = ''
get_indexes = ''
get_triggers = ''
get_view = ''
db = ''

def start():
    global get_tables
    global get_rows
    global get_table_query

    with sqlite3.connect(db) as conn:
        
        get_tables = conn.cursor().execute('select * from sqlite_master where type == "table"').fetchall()
        get_indexes = conn.cursor().execute('select * from sqlite_master where type == "index"').fetchall()
        get_triggers = conn.cursor().execute('select * from sqlite_master where type == "trigger"').fetchall()
        get_view = conn.cursor().execute('select * from sqlite_master where type == "view"').fetchall()


        
        def get_table_query(table :str) -> list:
            return list(_ for _ in conn.execute(f'Select * from {table}').fetchall())

        def get_rows(table : str) -> list:
            rows = conn.execute(f'PRAGMA table_info({table})').fetchall()
            table_rows = []
            for row in rows:
                row_name,type = row[1],row[2]
                table_rows.append(row_name)
            return table_rows
        return 

