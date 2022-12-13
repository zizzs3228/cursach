from asyncio import get_event_loop
import asyncio
import sqlite3
from aiogram import Bot, Dispatcher, executor
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
import sqlite3_controls
from credentials import bot_token, developer_id_1, developer_id_2, users_db_path, codes_db_path
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.dispatcher.filters import Command, Text
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton 
from aiogram.contrib.fsm_storage.memory import MemoryStorage 
import rarfile
import zipfile
import time
import os


bot_loop = asyncio.get_event_loop()

ibot = Bot(bot_token, parse_mode="HTML")
storage = MemoryStorage()
dp = Dispatcher(ibot, loop=bot_loop,storage=storage)
connection_to_users_db = None
connection_to_codes_db = None


codes=[]
ids=[]
end_times=[]

menu_1=ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="/accounts"), 
            KeyboardButton(text="/proxy"),
            KeyboardButton(text="/Myinfo"), 
        ],
        [
            KeyboardButton(text="/Parse")
        ]
             ],
    resize_keyboard=True
)


#reply_markup=ReplyKeyboardRemove()
class usersParse(StatesGroup):
    link = State()
    amount = State()

async def user_check_login(user_id: str) -> bool:
    cursor = connection_to_codes_db.cursor()
    
async def codes_synchronisation():
    table_name = 'users_codes'
    global codes 
    codes = await sqlite3_controls.table_get_codes(connection_to_codes_db,table_name)
    codes = [str(elem).replace('(','').replace(')','').replace(',','').replace("'",'',2) for elem in codes]


async def ids_synchronisation():
    table_name = 'users_codes'
    global ids
    ids = await sqlite3_controls.table_get_ids(connection_to_codes_db,table_name)
    ids = [str(elem).replace('(','').replace(')','').replace(',','').replace("'",'',2) for elem in ids]

async def end_times_synchronisation():
    global end_times
    end_times = await sqlite3_controls.table_get_ids(connection_to_codes_db,'users_codes','end_time','end_time')
    end_times = [int(str(elem).replace('(','').replace(')','').replace(',','').replace("'",'',2)) for elem in end_times]


async def time_is_up():
    for timing in end_times:
        if timing < time.time():
            await sqlite3_controls.table_delete_row(connection_to_codes_db,'users_codes',timing)
            await end_times_synchronisation()
            await ids_synchronisation()
    
    


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
    await end_times_synchronisation()
    print(end_times)
    await time_is_up()




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
    await time_is_up()
    if str(message.from_id) in ids:
        await message.answer('Загрузите текстовый(.txt) файл, в котором лежат прокси в формате IP:port:login:password',reply_markup=menu_1)
    else:
        await message.answer('Введите ваш инвайт-код, купив его на этом сайте (ссылка)')

@dp.message_handler(Command("accounts"))
async def accounts(message:Message):
    await time_is_up()
    if str(message.from_id) in ids:
        await message.answer('Загрузите архив(.zip или .rar) с аккаунтами, который вы купили. Если вам сайт прислал по одному, то упакуйте все ПАПКИ с файлами .session и .json в один архив и загрузите')
    else:
        await message.answer('Введите ваш инвайт-код, купив его на этом сайте (ссылка)')

@dp.message_handler(Command("Myinfo"))
async def Myinfo(message:Message):
    await time_is_up()
    if str(message.from_id) in ids:
        path = f'./files/{message.from_id}'
        proxy = []
        accscounter = 0
        for rootdir, dirs, files in os.walk(path):
            for file in files:
                if((file.split('.')[-1])=='txt'):
                    proxfile = open(os.path.join(rootdir, file))
                    proxy += proxfile.readlines()
                if((file.split('.')[-1])=='json'):
                    accscounter+=1
        proxy = [elem.strip() for elem in proxy]
        proxy = list(set(proxy))
        await message.answer(f'Вы загрузили {len(proxy)} уникальных прокси и {accscounter} аккаунтов')
        end_time = await sqlite3_controls.table_get_value_LUCHSE(connection_to_codes_db,'users_codes',message.from_id)
        if end_time is not None:
            end_time = int(str(end_time).replace('(','').replace(')','').replace(',',''))
            await message.answer(f'Ваша подписка истекает {time.ctime(end_time)}')
    else:
        await message.answer('Введите ваш инвайт-код, купив его на этом сайте (ссылка)')

@dp.message_handler(Command("Parse"))
async def set_users_parse(message:Message):
    await message.answer('Введите ссылку на чат, с которого вы хотите спарсить самых активных пользователей')
    await usersParse.link.set()

@dp.message_handler(state=usersParse.link)
async def get_link(message:Message,state:FSMContext):
    #https://t.me/SyndicateCryptocomchat
    link = message.text
    link = link.split('/')
    print(link)
    pseudolink = 'https://t.me/ijnsafljsngjn'
    pseudolink = pseudolink.split('/')
    print(pseudolink)
    if link[0]==pseudolink[0] and link[2]==pseudolink[2]:
        await state.update_data(link = message.text)
        await message.answer('Сколько активных человек спарсить из этого чата? Введите число от 1 до 10000')
        await usersParse.amount.set()
    else:
        await message.answer('Ссылка нерпавильная, введите её в формате https://t.me/')
        await usersParse.link.set()
    # await state.update_data(link = message.text)
    # await message.answer('Сколько активных человек спарсить из этого чата? Введите число от 1 до 10000')
    # await usersParse.amount.set()

@dp.message_handler(state=usersParse.amount)
async def get_amount(message:Message,state:FSMContext):
    await state.update_data(amount = message.text)
    data = await state.get_data()
    await message.answer(f'Вы хотите спарсить {data["amount"]} пользователей из {data["link"]}')
    await state.finish()


@dp.message_handler(content_types='document')
async def photo_or_doc_handler(message:Message):
    if str(message.from_id) in ids:
        file_name = message.document.file_name.split('.')
        if len(file_name)==2:
            file_destination = f'./files/{message.from_id}/{message.document.file_name}'
            if file_name[1]=='zip':
                await message.document.download(destination_file=file_destination)
                with zipfile.ZipFile(file_destination) as zip:
                    for file in zip.namelist():
                        if (".session" in file) or (".json" in file):
                            zip.extract(file, f'./files/{message.from_id}')
                os.remove(file_destination)
            elif file_name[1]=="rar":
                await message.document.download(destination_file=file_destination)
                with rarfile.RarFile(file_destination) as rar:
                    for file in rar.namelist():
                        if (".session" in file) or (".json" in file):
                            rar.extract(file, f'./files/{message.from_id}')
                os.remove(file_destination)
            elif file_name[1]=='txt':
                await message.document.download(destination_file=file_destination)
            else:
                await message.answer('Я могу принять только расширения .zip и .rar для архива с аккаунтами и только .txt для файла с прокси')
        else:
            await message.answer('Пришли, пожалуйста, файл с нормальным расширением по типу файл.txt файл.zip файл.rar')
    else:
        await message.answer('Введите ваш инвайт-код, купив его на этом сайте (ссылка)')

@dp.message_handler()
async def echo(message: Message):
    if str(message.from_id) not in ids:
        if message.text in codes:
            await message.answer('Вы ввели правильный инвайт-код',reply_markup=menu_1)
            await sqlite3_controls.table_update_value(connection_to_codes_db,'users_codes',"id",message.from_id,"code",f'"{message.text}"')
            await sqlite3_controls.table_update_value(connection_to_codes_db,'users_codes',"end_time",f'{int(time.time())}+duration',"code",f'"{message.text}"')
            await codes_synchronisation()
            print(codes)
            await ids_synchronisation()
            print(ids)
            await end_times_synchronisation()
            print(end_times)
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