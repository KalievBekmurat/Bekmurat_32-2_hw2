from decouple import config
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage()
TGBOTtoken = config('TGBOTtoken')
bot = Bot(token=TGBOTtoken)
dp = Dispatcher(bot=bot, storage=storage)