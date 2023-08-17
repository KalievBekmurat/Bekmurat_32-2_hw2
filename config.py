from decouple import config
from aiogram import Bot, Dispatcher

TGBOTtoken = config('TGBOTtoken')
bot = Bot(token=TGBOTtoken)
dp = Dispatcher(bot=bot)