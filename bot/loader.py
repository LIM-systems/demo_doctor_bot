import logging
import pathlib

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

path = pathlib.Path().absolute()
bot = Bot(token='5641543913:AAGjZSL6GzP_AeWARz8YtmHk-bIaav-A-pY', parse_mode='HTML')
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

main_menu = ('▪ Запись к врачу', '▪ О нас', '▪ Мои записи')
app_docs = ('🌀 Записаться на прием', '<< Назад к списку')
back = '<< Назад'
cancel = '❌ Отменить'

#logger = logging.getLogger(__name__)
#logging.basicConfig(
    #filename=f'{path}/logs/logger.log',
    #level=logging.ERROR,
    #format='%(asctime)s, %(levelname)s, %(name)s, %(message)s',
#)
#logger.addHandler(logging.StreamHandler())
