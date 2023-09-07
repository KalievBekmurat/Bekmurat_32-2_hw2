import random
import re

#from scraping.Films_Scraper import FilmsScraper

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from config import bot
from aiogram import types, Dispatcher

from database.sql_commands import Database
from keyboards.start_kb import like_dislike_keyboard, my_profile_detail_keyboard, if_not_profile_keyboard
#save_films_keyboard


async def admin_user_call(call: types.CallbackQuery):
    users = Database().sql_admin_select_user_command()
    print(users)
    data = []
    for user in users:
        if not user["username"]:
            data.append(f"[{user['first_name']}](tg://user?id={user['telegram_id']})")
        else:
            data.append(f"[{user['username']}](tg://user?id={user['telegram_id']})")

    data = '\n'.join(data)
    await call.message.reply(text=data, parse_mode=types.ParseMode.MARKDOWN)


async def my_profile_call(call: types.CallbackQuery):
    user_form = Database().sql_select_user_form_by_telegram_id_command(
        telegram_id=call.from_user.id)
    print(user_form)
    try:
        with open(user_form[0]["photo"], 'rb') as photo:
            await bot.send_photo(
                chat_id=call.message.chat.id,
                photo=photo,
                caption=f"*Nickname:* {user_form[0]['nickname']}\n"
                        f"*Age:* {user_form[0]['age']}\n"
                        f"*bio:* {user_form[0]['bio']}\n"
                        f"*married:* {user_form[0]['married']}\n",
                parse_mode=types.ParseMode.MARKDOWN,
                reply_markup=await my_profile_detail_keyboard()
            )
    except IndexError as e:
        await bot.send_message(
            chat_id=call.message.chat.id,
            text="Вы не зарегистрированы можете нажать на кнопку и зарегистрироваться",
            reply_markup=await if_not_profile_keyboard()
        )


async def random_profiles_call(call: types.CallbackQuery):
    user_forms = Database().sql_select_user_forms_command()
    print(user_forms)
    random_form = random.choice(user_forms)
    print(random_form)
    with open(random_form["photo"], 'rb') as photo:
        await bot.send_photo(
            chat_id=call.message.chat.id,
            photo=photo,
            caption=f"*Nickname:* {random_form['nickname']}\n"
                    f"*Age:* {random_form['age']}\n"
                    f"*bio:* {random_form['bio']}\n"
                    f"*married:* {random_form['married']}\n",
            parse_mode=types.ParseMode.MARKDOWN,
            reply_markup=await like_dislike_keyboard(
                telegram_id=random_form["telegram_id"]
            )
        )


async def like_call(call: types.CallbackQuery):
    owner_telegram_id = re.sub("like_button_", "", call.data)
    is_like_existed = Database().sql_select_liked_form_command(
        owner_telegram_id=owner_telegram_id,
        liker_telegram_id=call.from_user.id
    )
    if is_like_existed:
        await bot.send_message(
            chat_id=call.message.chat.id,
            text="Ты уже лайкал эту анкету"
        )
    else:
        Database().sql_insert_like_form_command(
            owner_telegram_id=owner_telegram_id,
            liker_telegram_id=call.from_user.id
        )
        await bot.send_message(
            chat_id=owner_telegram_id,
            text=f"Кому то понравилась твоя анкета \nМожешь перейти по ссылке и пообщаться [{call.from_user.first_name}](tg://user?id={call.from_user.id})",
            parse_mode=types.ParseMode.MARKDOWN_V2

        )


    await random_profiles_call(call=call)

async def dislike_call(call: types.CallbackQuery):
    owner_telegram_id = re.sub("dislike_button_", "", call.data)
    is_like_existed = Database().sql_select_liked_form_command(
        owner_telegram_id=owner_telegram_id,
        disliker_telegram_id=call.from_user.id

    )
    if is_like_existed:
        await bot.send_message(
            chat_id=call.message.chat.id,
            text="Ты уже лайкал эту анкету"
        )
    else:
        Database().sql_insert_like_form_command(
            owner_telegram_id=owner_telegram_id,
            liker_telegram_id=call.from_user.id
        )
        await bot.send_message(
            chat_id=owner_telegram_id,
            text=f"Кому-то не понравилась твоя анкета \nМожешь перейти по ссылке и  спросить почему ты не нравишься [{call.from_user.first_name}](tg://user?id={call.from_user.id})",
            parse_mode=types.ParseMode.MARKDOWN_V2
        )

async def delete_profile_call(call: types.CallbackQuery):
    Database().sql_delete_user_form(telegram_id=call.from_user.id)
    await bot.send_message(
        chat_id=call.message.chat.id,
        text="Deleted Successfully"
    )



# async def films_parsing_call(call: types.CallbackQuery):
#     scraper = FilmsScraper()
#     data = scraper.parse_data()
#     for url in data:
#         Database().sql_insert_films_command(link=url)
#         films_id = Database().sql_select_specific_films_command(link=url)
#         print(films_id[0]['id'])
#         await bot.send_message(
#             chat_id=call.message.chat.id,
#             text=url,
#             reply_markup=await save_films_keyboard(films_id=films_id[0]['id'])
#         )
#
#
# async def save_films_call(call: types.CallbackQuery):
#     films_id = re.sub("save_films_", "", call.data)
#     link = Database().sql_select_specific_films_for_favourite_command(
#         films_id=films_id
#     )
#     print(link[0]["link"])
#     Database().sql_insert_favourite_films_command(
#         owner_telegram_id=call.from_user.id,
#         link=link[0]["link"]
#     )
#     await bot.send_message(
#         chat_id=call.message.chat.id,
#         text="Вы сохранили фильм"
#     )
#
#
# async def my_films_call(call: types.CallbackQuery):
#     links = Database().sql_select_owner_films_command(
#         owner_telegram_id=call.from_user.id
#     )
#     for link in links:
#         await bot.send_message(
#             chat_id=call.message.chat.id,
#             text=link['link']
#         )

def register_callback_handlers(dp: Dispatcher):

    dp.register_callback_query_handler(admin_user_call, lambda call: call.data == "admin_user_list")
    dp.register_callback_query_handler(my_profile_call, lambda call: call.data == "my_profile")
    dp.register_callback_query_handler(random_profiles_call, lambda call: call.data == "random_profiles")
    dp.register_callback_query_handler(like_call, lambda call: "like_button_" in call.data)
    dp.register_callback_query_handler(delete_profile_call, lambda call: call.data == "delete_profile")
    # dp.register_callback_query_handler(films_parsing_call, lambda call: call.data == "films_parsing")
    # dp.register_callback_query_handler(save_films_call, lambda call: "save_films_" in call.data)
    # dp.register_callback_query_handler(my_films_call, lambda call: call.data == "my_films_call_data")