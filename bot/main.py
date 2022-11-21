from aiogram import executor, types

import handlers
import keyboards
from loader import dp

if __name__ == '__main__':
    executor.start_polling(dp)