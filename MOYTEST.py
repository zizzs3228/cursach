import json
from telethon import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest, ImportChatInviteRequest, CheckChatInviteRequest, AddChatUserRequest
from telethon.tl.functions.channels import JoinChannelRequest, LeaveChannelRequest, GetParticipantsRequest, InviteToChannelRequest,GetFullChannelRequest
from telethon.tl.types import InputPeerEmpty
from telethon.tl.types import ChannelParticipantsSearch, ChannelParticipantsRecent
import time
import sqlite3_controls
import random

db_name = 'cursach.db'

with open('./accs/+6285794040091/+6285794040091.json') as f:
    file_content = f.read()
    templates = json.loads(file_content)
    

phone = templates.get("phone")
app_id = templates.get("app_id")
app_hash = templates.get("app_hash")
    

client = TelegramClient('./accs/+6285794040091/+6285794040091', app_id, app_hash)



async def invite(link:str, amount:int, user_id:str) -> None:
    channel = await client.get_entity(link)
    db_connection = await sqlite3_controls.database_connect(db_name)
    current_user = []
      
    
    for i in range(0,amount):
        current_user = await sqlite3_controls.table_fetch_first(db_connection, user_id)
        if current_user:
            if channel.megagroup:
                try:
                    print((current_user[0],))
                    #await client(InviteToChannelRequest(channel, (current_user[0],)))
                    #time.sleep(random.uniform(20,40))
                    pass
                except: 
                    continue
            else:
                try:
                    print((current_user[0],'Ы'))
                    await client(AddChatUserRequest(channel.id, current_user[0],fwd_limit=500))
                    print(f"Пользователь {current_user[0]} приглашён")
                    time.sleep(random.uniform(20,40))
                except: 
                    continue
        else:
            print("We run out of users!")
            return None
            
        

async def parse(link:str, user_id:str) -> None:
    channel = await client.get_entity(link)
    channel_info = await client(GetFullChannelRequest(channel=channel))
    db_connection = await sqlite3_controls.database_connect(db_name)
    await sqlite3_controls.database_create_table(db_connection, user_id)
    await client(JoinChannelRequest(channel))
    # all_participants=[]
    # offset = 0
    # limit = 5000
    # participants = await client(GetParticipantsRequest(
    #     channel, ChannelParticipantsRecent(), offset, limit,
    #     hash=0))
    # all_participants.extend(participants.users)
    # print(participants)
        # print(participants)
    #participant = []
    number_of_participants = channel_info.full_chat.participants_count
    async for user in client.iter_participants(channel, limit=3000):
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
            await sqlite3_controls.table_insert_values(db_connection,user_id,(user.id,username,name,phone))
    db_connection.close()
    print("Пользователи собраны")

    

async def main():
    #await client.send_message('@SemadiD', 'Тест')
    #chat = await client.get_entity('https://t.me/SpamBot')
    # async for message in client.iter_messages(chat):
    #     print(message.message)

    
    #channel = await client.get_entity('https://t.me/SyndicateCryptocomchat')
    #await parse('https://t.me/okxofficial_ru', 'users1')
    await invite('https://t.me/SyndicateTradingChat',20,'users1')
    
    
    # print(channel)
    #await parse('https://t.me/satoshifriends')
    # db = await sqlite3_controls.database_connect(db_name)
    # for i in range(1,50):
    #     print(await sqlite3_controls.table_fetch_first(db, 'users1'))
    # for name in niks:
    #     user_tuple = await user_get_id(db_cursor,name)
    #     user_id=user_tuple[0]
    #     print(user_id)
    # invite = True
    # rassilka = False
    # for name in niks:
    #     user_tuple = await user_get_id(db_cursor,name)
    #     user_id=int(user_tuple[0])
    #     if invite:
    #         if channel.megagroup == False:
    #             try:
    #                 await client(InviteToChannelRequest(channel, user_id))
    #                 print(f"Приглашен пользователь {user_id} в канал")
    #                 time.sleep(30)
    #             except: 
    #                 continue
    #         else:
    #             try:
    #                 await client(AddChatUserRequest(channel.id, user_id,fwd_limit=10))
    #                 print(f"Приглашен пользователь {user_id} в чат")
    #                 time.sleep(30)
    #             except: 
    #                 continue
    #     elif rassilka:
    #         await client.send_message(user_id, 'test botika')
    #         time.sleep(10)
    pass

    


    
    

    # conn = sqlite3.connect('cursach.db')


    # with open("members.csv","w",encoding='UTF-8') as f:
    #     writer = csv.writer(f,delimiter=",",lineterminator="\n")
    #     writer.writerow(['username','user id', 'access hash','name','group', 'group id','phone'])
    #     for user in all_participants[:100]:
    #         if user.phone:
    #             phone = user.phone
    #         else:
    #             phone=""
    #         if user.username:
    #             username= user.username
    #         else:
    #             username= ""
    #         if user.first_name:
    #             first_name= user.first_name
    #         else:
    #             first_name= ""
    #         if user.last_name:
    #             last_name= user.last_name
    #         else:
    #             last_name= ""
    #         name= (first_name + ' ' + last_name).strip()
    #         writer.writerow([username,user.id,user.access_hash,name,channel.title, channel.id, phone]) 
    #participants = await client(GetParticipantsRequest(channel,filter,offset_user, limit_user, hash=0))
    #print(await client(CheckChatInviteRequest('+2-gY_VGDB4lmZmQy')))
   # updates = await client(ImportChatInviteRequest('https://t.me/SyndicateCryptocomchat'))
    #https://t.me/+2-gY_VGDB4lmZmQy
    #print(channel.usernames)
    



    # contact = await client.get_entity('+34xxxxxxxxx')
    # friend  = await client.get_entity(friend_id)


    
    #await client.send_message('zizzs3228', '')
    # result = client(GetDialogsRequest(
    #          offset_date=last_date,
    #          offset_id=0,
    #          offset_peer=InputPeerEmpty(),
    #          limit=chunk_size,
    #          hash = 0
    #      ))
    # chats.extend(result.chats)
 
    # for chat in chats:
    #     try:
    #         if chat.megagroup== True:
    #             groups.append(chat)
    #     except:
    #         continue
 
    # print('[+] Choose a group to scrape members :')
    # i=0
    # for g in groups:
    #     print('['+str(i)+']'' - '+ g.title)
    #     i+=1
    

with client:
    client.loop.run_until_complete(main())
    # client.loop.run_until_complete(payload(client))
    # for task in asyncio.Task.all_tasks(client.loop):
    #     task.cancel()
    
