from asyncio import get_event_loop
import asyncio
import sqlite3
from aiogram import Bot, Dispatcher, executor, types
import sqlite3_controls
from credentials import bot_token, developer_id_1, developer_id_2, users_db_path, codes_db_path
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.dispatcher.filters import Command, Text
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import archive_management
import time

bot_loop = asyncio.get_event_loop()

ibot = Bot(bot_token, parse_mode="HTML")

dp = Dispatcher(ibot, loop=bot_loop)
connection_to_users_db = None
connection_to_codes_db = None

codes=[]
ids=[]

menu_1=ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="/accounts"), 
            KeyboardButton(text="/proxy")
        ]
             ],
    resize_keyboard=True
)


#reply_markup=ReplyKeyboardRemove()

print(codes)
print(ids)

async def user_check_login(user_id: str) -> bool:
    cursor = connection_to_codes_db.cursor()
    
async def codes_synchronisation():
    table_name = 'users_codes'
    global codes 
    codes = await sqlite3_controls.table_get_codes(connection_to_codes_db,table_name)
    codes = [str(elem).replace('(','').replace(')','').replace(',','').replace("'",'',2) for elem in codes]
    print("Лист кодов успешно изменён")


async def ids_synchronisation():
    table_name = 'users_codes'
    global ids
    ids = await sqlite3_controls.table_get_ids(connection_to_codes_db,table_name)
    ids = [str(elem).replace('(','').replace(')','').replace(',','').replace("'",'',2) for elem in ids]
    print("Лист айдишников успешно изменён")

async def start_up_preparations(dp):
    # await ibot.send_message(chat_id= developer_id_2,text="Initiating sequence complete. Bot is online.")
    # await ibot.send_message(chat_id=developer_id_1, text="Initiating sequence complete. Bot is online.")
    global connection_to_users_db 
    connection_to_users_db = await sqlite3_controls.database_connect(users_db_path)
    global connection_to_codes_db 
    connection_to_codes_db = await sqlite3_controls.database_connect(codes_db_path)
    await codes_synchronisation()
    print(codes)
    await ids_synchronisation()
    print(ids)


async def shut_down_warning(dp):
#    await ibot.send_message(chat_id=developer_id_2, text="Termination order recieved. Shutting down.",reply_markup=ReplyKeyboardRemove())
#    await ibot.send_message(chat_id=developer_id_1, text="Termination order recieved. Shutting down.",reply_markup=ReplyKeyboardRemove())
    pass
   #H78b4O
#reply_markup=menu_1

@dp.message_handler(Command("start"))
async def start(message:Message):
    print(f"From {message.from_user} recieved {message.text}")
    await message.answer(f"Здравствуйте {message.from_user.first_name}, введите инвайт-код с этого сайта (ссылка)")


@dp.message_handler(Command("proxy"))
async def proxy(message:Message):
    if str(message.from_id) in ids:
        await message.answer('Загрузите текстовый(.txt) файл, в котором лежат прокси в формате IP:port:login:password')
    else:
        await message.answer('Введите ваш инвайт-код, купив его на этом сайте (ссылка)')

@dp.message_handler(Command("accounts"))
async def proxy(message:Message):
    if str(message.from_id) in ids:
        await message.answer('Загрузите архив(.zip или .rar) с аккаунтами, который вы купили. Если вам сайт прислал по одному, то упакуйте все ПАПКИ с файлами .session и .json в один архив и загрузите')
    else:
        await message.answer('Введите ваш инвайт-код, купив его на этом сайте (ссылка)')

@dp.message_handler(content_types=['document'])
async def photo_or_doc_handler(message: types.Message):
    file_name = message.document.file_name.split('.')
    file_destination = f'./{message.from_id}/{message.document.file_name}'
    await message.document.download(destination_file=file_destination)

@dp.message_handler()
async def echo(message: Message):
    if message.text in codes:
        await message.answer('Вы ввели правильный инвайт-код',reply_markup=menu_1)
        await sqlite3_controls.table_update_value(connection_to_codes_db,'users_codes',"id",message.from_id,"code",f'"{message.text}"')
        await sqlite3_controls.table_update_value(connection_to_codes_db,'users_codes',"end_time",f'{int(time.time())}+duration',"code",f'"{message.text}"')
        await codes_synchronisation()
        print(codes)
        await ids_synchronisation()
        print(ids)
    else:
        await message.answer('Введите ваш инвайт-код, купив его на этом сайте (ссылка)')

        
    
if __name__ == "__main__":
    
    executor.start_polling(dp, on_startup=start_up_preparations, on_shutdown=shut_down_warning)
    
    
#start 
#aboba
#----accs
#----proxy
#
#user_id code duration last_login 