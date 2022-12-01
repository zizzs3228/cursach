import sqlite3_controls
import asyncio

async def main():
    db_name = "./invites-code.db"
    table_name = "users_codes"
    connection = await sqlite3_controls.database_connect(db_name)
    await sqlite3_controls.table_insert_values(connection, table_name, (1, "test", 1, 1))
    await sqlite3_controls.table_update_value(connection,table_name,"id",1,"last_login",2)
    print(await sqlite3_controls.table_fetch_first(connection,table_name))

if __name__ == "__main__":
    asyncio.run(main())