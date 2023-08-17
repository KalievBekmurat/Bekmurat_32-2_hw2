from config import bot
from aiogram import types, Dispatcher
from database import sql_commands
from const import START_MENU_TEXT


async def start_button(message: types.Message):
    sql_commands.Database().sql_insert_user_cmd(
        telegram_id=message.from_user.id,
        username=message.from_user.username,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name)

    print(message)
    await message.reply('Приветик !'
                        'Я являюсь Админ ботом который банит за матюки')



def register_start_handler(dp: Dispatcher):
    dp.register_message_handler(start_button, commands=['start'])