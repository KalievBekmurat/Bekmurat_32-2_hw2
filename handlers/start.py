from aiogram.utils.deep_linking import _create_link

from config import bot
from aiogram import types, Dispatcher

from const import START_MENU_TEXT
from database import sql_commands
from database.sql_commands import Database
from keyboards.start_kb import admin_select_users_keyboard, start_keyboard, new_start_keyboard

async def start_button(message: types.Message):
    command = message.get_full_command()
    print(command)
    if command[1] != "":
        existed_user = Database().sql_select_existed_reference_command(
            reference_telegram_users=message.from_user.id
        )
        print(existed_user)
        if not existed_user:
            link = await _create_link(link_type="start", payload=command[1])
            owner = Database().sql_select_owner_link_command(
                owner_link=link
            )
            print(owner)
            Database().sql_insert_reference_users(
                owner_telegram_id=owner[0]["telegram_id"],
                reference_telegram_users=message.from_user.id
            )
        else:
            pass
    sql_commands.Database().sql_insert_user_command(
        telegram_id=message.from_user.id,
        username=message.from_user.username,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name,
    )

    print(message)
    with open("C:\Bekmurat_32-2_hw2\media\FF.jpg", "rb") as photo:
        await bot.send_photo(
            chat_id=message.chat.id,
            photo=photo,
            caption=START_MENU_TEXT.format(
                user=message.from_user.username
            ),
            parse_mode=types.ParseMode.MARKDOWN,
            reply_markup=await new_start_keyboard()
        )













def register_start_handlers(dp: Dispatcher):
    dp.register_message_handler(start_button, commands=['start'])
