import sqlite3_controls
import asyncio

async def main():
    db_name = "./invites-code.db"
    table_name = "users_codes"
    connection = await sqlite3_controls.database_connect(db_name)
    #codes = await sqlite3_controls.table_get_codes(connection,table_name)
    cursor = connection.cursor()
    print("Подключен к SQLite")
    sqlite_select_query = """SELECT code FROM users_codes WHERE id IS NULL"""
    cursor.execute(sqlite_select_query)
    records = cursor.fetchall()
    print("Всего строк:  ", len(records))
    print("Вывод каждой строки")
    print(records)

    
    #await sqlite3_controls.table_update_value(connection,table_name,'id','468424685','code','"H78b40"')
    # await sqlite3_controls.table_insert_values(connection, table_name, (1, "test", 1, 1))
    # await sqlite3_controls.table_update_value(connection,table_name,"id",1,"last_login",2)
    #print(await sqlite3_controls.table_fetch_first(connection,table_name))
    
if __name__ == "__main__":
    asyncio.run(main())