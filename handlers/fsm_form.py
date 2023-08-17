from aiogram.dispatcher import FSMContext
from aiogram.types import ContentTypes


from config import bot
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup
from database.sql_commands import Database



class Form_States(StatesGroup):
    nickname = State()
    age = State()
    bio = State()
    married = State()
    photo = State()

async def fsm_start(message: types.Message):
    await message.reply('Отправьте свой никнейм:')
    await Form_States.nickname.set()

async def load_nickname(message: types.Message,
                        state: FSMContext):
    async with state.proxy() as data:
        data['nickname'] = message.text


    await Form_States.next()
    await message.reply('Отправьте свой возраст (используя числа):')


async def load_age(message: types.Message,
                   state: FSMContext):
    try:
        if type(int(message.text)) != int:
            await message.reply('              🔴Ошибка🔴'
                                'Отправьте свой возраст (ИСПОЛЬЗУЯ ЧИСЛА)'
                                '      Запустите регистрацию заново')
            await state.finish()
        else:
            async with state.proxy() as data:
                data['age'] = message.text
            await Form_States.next()
            await message.reply('Отправьте свое место рождения:')
    except ValueError as e:
        await state.finish()
        print(f'FSMAGE: {e}')
        await message.reply('              🔴Ошибка🔴'
                                'Отправьте свой возраст (ИСПОЛЬЗУЯ ЧИСЛА)'
                                '      Запустите регистрацию заново')

async def load_bio(message: types.Message,
                    state: FSMContext):
    async with state.proxy() as data:
        data['bio'] = message.text

    await Form_States.next()
    await message.reply("Отправьте свою биографию:")


async def load_married(message: types.Message,
                   state: FSMContext):
    async with state.proxy() as data:
        data['married'] = message.text

    await Form_States.next()
    await message.reply("Отправьте свою фотографию: ")


async def load_photo(message: types.Message,
                     state: FSMContext):
    print(message.photo)
    path = await message.photo[-1].download(
        destination_dir="C:\Bekmurat_32-2_hw2\media"
    )
    async with state.proxy() as data:
        with open(path.name, 'rb') as photo:
            await bot.send_photo(
                chat_id=message.chat.id,
                photo=photo,
                caption=f'Nickname: {data["nickname"]}\n'
                        f'Age: {data["age"]}\n'
                        f'bio: {data["bio"]}\n'
                        f'married: {data["married"]}\n'
            )


def register_fsm_form_handlers(dp: Dispatcher):
    dp.register_message_handler(fsm_start, commands=["signup"])
    dp.register_message_handler(load_nickname,
                                state=Form_States.nickname,
                                content_types=['text'])
    dp.register_message_handler(load_age,
                                state=Form_States.age,
                                content_types=['text'])
    dp.register_message_handler(load_bio,
                                state=Form_States.bio,
                                content_types=['text'])
    dp.register_message_handler(load_married,
                                state=Form_States.married,
                                content_types=['text'])
    dp.register_message_handler(load_photo,
                                state=Form_States.photo,
                                content_types=ContentTypes.PHOTO)