import datetime
from config import bot
from aiogram import types, Dispatcher
from const import START_MENU_TEXT
from database import sql_commands

# START_MENU_TEXT = '''
# Привет дорогой пользователь{user}
# 👮‍♂️ слежу за порядком и чистотой в чате ,блокирую неадекватов в группе за маты '''

async def echo_ban(message: types.Message):
    ban_words = ['стриптизерша','damn', 'fuck', 'bitch', 'freak', 'fuck you', 'gay', 'nigger', 'shit', 'whore', 'poop', 'сука', 'блять', 'пиздец', 'дурак', 'дура', 'мразь', 'шалава']

    if message.chat.id == -1001936389612:
        for word in ban_words:
            if word in message.text.lower().replace(" ", " "):
                await bot.delete_message(
                    chat_id=message.chat.id,
                    message_id=message.message_id)
                await bot.send_message(
                    chat_id=message.chat.id,
                    text=f"❌Запрещено писать нецензурную брань!❌\n"
                         f" Сука воздержись от такого поведения в чате!\n"
                         f"_______________________________________"
                         f'🔴Пользователь {message.from_user.username}🔴')


def register_chat_actions_handlers(dp: Dispatcher):
    dp.register_message_handler(echo_ban)