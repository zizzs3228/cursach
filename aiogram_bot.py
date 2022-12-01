from asyncio import get_event_loop
import asyncio
from aiogram import Bot, Dispatcher, executor
from sqlalchemy import asc
from credentials import bot_token, developer_id_1, developer_id_2
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.dispatcher.filters import Command, Text
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

bot_loop = asyncio.get_event_loop()

ibot = Bot(bot_token, parse_mode="HTML")

dp = Dispatcher(ibot, loop=bot_loop)


menu_1=ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Politics") , 
            KeyboardButton(text="Traveling")
        ],
        [
            KeyboardButton(text="Economy"),
            KeyboardButton(text="News")
        ],
        [
            KeyboardButton(text="Science"),
            KeyboardButton(text="Culture")
        ],
        [
            KeyboardButton(text="Wildlife"),
            KeyboardButton(text="Religion")
        ]
             ],
    resize_keyboard=True
)


#reply_markup=ReplyKeyboardRemove()

async def start_up_warning(dp):
    # await ibot.send_message(chat_id= developer_id_2,text="Initiating sequence complete. Bot is online.")
    # await ibot.send_message(chat_id=developer_id_1, text="Initiating sequence complete. Bot is online.")
    pass

async def shut_down_warning(dp):
#    await ibot.send_message(chat_id=developer_id_2, text="Termination order recieved. Shutting down.",reply_markup=ReplyKeyboardRemove())
#    await ibot.send_message(chat_id=developer_id_1, text="Termination order recieved. Shutting down.",reply_markup=ReplyKeyboardRemove())
    pass
   
#reply_markup=menu_1

@dp.message_handler(Command("start"))
async def show_menu_1(message:Message):
    print(f"From {message.from_user} recieved {message.text}")
    text=f"Здравствуйте {message.from_user.first_name}, введите инвайт-код с этого сайта (ссылка)"
    await ibot.send_message(chat_id=message.from_user.id, text=text, )

@dp.message_handler()
async def echo(message: Message):
    await message.answer('введите инвайт-код с этого сайта (ссылка)')
    
if __name__ == "__main__":
    
    executor.start_polling(dp, on_startup=start_up_warning, on_shutdown=shut_down_warning)
    
    
