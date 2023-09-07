from decouple import config
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

PROXY_URL = "http://proxy.server.3128"



storage = MemoryStorage()
TGBOTtoken = config('TGBOTtoken')
bot = Bot(token=TGBOTtoken,proxy=PROXY_URL)
dp = Dispatcher(bot=bot, storage=storage)