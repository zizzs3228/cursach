import sqlite3_controls
import json
import os
import time
import asyncio
from credentials import users_db_path
from telethon import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest, ImportChatInviteRequest, CheckChatInviteRequest, AddChatUserRequest
from telethon.tl.functions.channels import JoinChannelRequest, LeaveChannelRequest, GetParticipantsRequest, InviteToChannelRequest,GetFullChannelRequest
from telethon.tl.types import InputPeerEmpty
from telethon.tl.types import ChannelParticipantsSearch, ChannelParticipantsRecent

client = None

async def proxymaker(proxystr:str)->dict:
    proxylist = ['proxy_type','addr','port','username','password']
    proxystr = 'socks5:'+proxystr.strip()
    proxystr = proxystr.split(':')
    proxystr[2] = int(proxystr[2])
    return dict(zip(proxylist,proxystr))
    






async def fs_manager(id:int, get_proxy:bool) -> str:
    path = f"/home/zizzs/cursach/files/{id}" 
    proxy_list = []
    if get_proxy:
        with open(path+"/proxy.txt", 'r') as proxy:
            proxy.seek(0)
            for line in proxy:
                proxy_list.append(line)
                #print(line)
            proxy.close()
        with open(path+"/proxy.txt", 'w') as proxy:      
            try:
                proxy_to_return = proxy_list.pop(0)
                proxy.writelines(proxy_list)
                proxy.flush()
                return proxy_to_return
            except IndexError as error:
                print(error)
                return None
    else:
        for rootdir, dirs, files in os.walk(path):
            for file in files:
                if((file.split('.')[-1])=='json'):
                    #return os.path.join(rootdir, file)
                    return rootdir+"/"+file
        return None


async def form_client(source_user_id:int) -> TelegramClient:
    
    path_to_folder = await fs_manager(source_user_id, False)

    if path_to_folder:
        client_name = path_to_folder.split('/')[-1]
        with open(path_to_folder) as f:
            file_content = f.read()
            acc_stats = json.loads(file_content)
        
        phone = acc_stats.get("phone")
        app_id = acc_stats.get("app_id")
        app_hash = acc_stats.get("app_hash")
        print(f"{path_to_folder} \n {client_name} \n {phone} {app_id} {app_hash}")
    else:
        print("Error while forming a client")
    
    proxy = await fs_manager(source_user_id, True)
    formed_proxy = await proxymaker(proxy)
    # path_to_folder[:-5]
    global client 
    client = TelegramClient(path_to_folder[:-5], int(app_id), app_hash, proxy=formed_proxy)
    # print(path_to_folder[:-5])
    # print(formed_proxy)

    return client


if __name__ == "__main__":
    asyncio.run(form_client(468424685))




async def parse(link_to_parse:str, user_id:str, parse_limit:int) -> None:
  
    
    client = await form_client(user_id)
    await client.start()
    channel_to_parse = await client.get_entity(link_to_parse)
    channel_info = await client(GetFullChannelRequest(channel=channel_to_parse))
    #db_connection = await sqlite3_controls.database_connect("/cursach.db")
    db_connection = await sqlite3_controls.database_connect(users_db_path)
    table_name = str(user_id)
    if not (await sqlite3_controls.database_create_table(db_connection, table_name)):
        await sqlite3_controls.table_flush(db_connection, table_name)
    
    await client(JoinChannelRequest(channel_to_parse))
    number_of_participants = channel_info.full_chat.participants_count
    async for user in client.iter_participants(channel_to_parse, limit=parse_limit):
        if user.phone:
            phone = user.phone
        else:
            phone=""
        if user.username:
            username= user.username
        else:
            username= ""
        if user.first_name:
            first_name= user.first_name
        else:
            first_name= ""
        if user.last_name:
            last_name= user.last_name
        else:
            last_name= ""
        name= (first_name + ' ' + last_name).strip()
        if name:
            await sqlite3_controls.table_insert_values(db_connection,table_name,(user.id,username,name,phone))
    db_connection.close()
    print("Пользователи собраны")
    await client.disconnect()

async def invite(chat_to_invite:str, user_id:str, invite_limit:int, invite_pace:int = 300) -> bool:
    db_connection = await sqlite3_controls.database_connect(users_db_path)
    current_user = []
    client = await form_client(user_id)
    await client.start()
    channel = await client.get_entity(chat_to_invite)
    if not channel.megagroup:
        print("User {user_id} provided link to channel!")
        await client.disconnect()
        return False
    else:
        for i in range(0, invite_limit):
            current_user = await sqlite3_controls.table_fetch_first(db_connection, user_id)
            if current_user:
                try:
                    #await client(AddChatUserRequest(channel.id, current_user[0],fwd_limit=500))
                    print(f"Пользователь {current_user[0]} приглашён в {channel.id}")
                    #time.sleep(invite_pace)
                except: 
                    print(f"Пользователь {current_user[0]} не может быть приглашен")
            else:
                print("We run out of users!")
        await client.disconnect()
        return True