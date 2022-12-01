import sqlite3


async def database_connect(db_path: str) -> sqlite3.Connection:
    try:
        database=sqlite3.connect(database=db_path)
        print(f"Database {db_path} connection established!")
        return database
    except sqlite3.Error as error:
        print(f"Database {db_path} connection failed! Error: {error}")
        return None

async def database_create_table(db_connection: sqlite3.Connection, table_name: str) -> bool:
    cursor = db_connection.cursor()
    
    sql_statement= """CREATE TABLE %s (id INTEGER NOT NULL UNIQUE, username TEXT, name TEXT, phone TEXT) """ % table_name
    try:
        cursor.execute(sql_statement)
        print("Successfully created a new table!")
        db_connection.commit()
        return True
    except sqlite3.Error as error:
        print(f"Failed to create a new table! Error: {error}")
        return False

async def table_insert_values(db_connection: sqlite3.Connection, table_name: str, values: list) -> bool:  
    cursor = db_connection.cursor()
    sql_statement = """INSERT INTO %s VALUES (?,?,?,?)""" % table_name
    try:
        cursor.execute(sql_statement,(values[0],values[1],values[2],values[3],))
        db_connection.commit()
        return True
    except sqlite3.Error as error:
        print(f"Failed to insert into {table_name}! Error: {error}")
        return False

async def table_get_value(db_connection: sqlite3.Connection, table_name: str, value, field:str = 'id') -> list:
    cursor = db_connection.cursor()
    sql_statement = """SELECT * FROM %s WHERE %s = (?)""" % (table_name, field)
    try:
        cursor.execute(sql_statement,(value,))
        result = cursor.fetchone()
        return result
    except sqlite3.Error as error:
        print(f"Failed to fetch {field} from {table_name}! Error: {error}")
        return None

async def table_delete(db_connection: sqlite3.Connection, table_name: str) -> bool:
    cursor = db_connection.cursor()
    sql_statement = """DROP TABLE %s""" % table_name
    try:
        cursor.execute(sql_statement)
        print(f"Table {table_name} successfully deleted!")
        db_connection.commit()
        return True
    except sqlite3.Error as error:
        print(f"Failed to delete {table_name}! Error: {error}")
        return False

async def table_fetch_first(db_connection: sqlite3.Connection, table_name: str) -> list:
    cursor = db_connection.cursor()
    sql_statement = """SELECT * FROM %s ORDER BY ROWID ASC LIMIT 1""" % table_name
    sql_statement2 = """DELETE FROM %s ORDER BY ROWID ASC LIMIT 1""" % table_name
    try:
        cursor.execute(sql_statement)
        result = cursor.fetchone()
        cursor.execute(sql_statement2)
        db_connection.commit()
        return result
    except sqlite3.Error as error:
        print(f"Failed to fetch from {table_name}! Error: {error}")
        return None

async def table_update_value(db_connection: sqlite3.Connection, table_name: str, search_field: str, search_field_value: str, field: str, new_value: str) -> bool:
    cursor = db_connection.cursor()
    sql_statement = """UPDATE %s SET %s = %s WHERE %s = %s""" % (table_name,field,new_value,search_field,search_field_value)
    try:
        cursor.execute(sql_statement)
        db_connection.commit()
        return True
    except sqlite3.Error as error:
        print(f"Failed to update field {field}! Error: {error}")
        return False