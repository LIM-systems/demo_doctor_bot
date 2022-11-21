from aiogram.dispatcher.filters.state import State, StatesGroup


class Docs(StatesGroup):
    '''Сохранение состояний'''
    special = State()
    doctor = State()
    doctor_id = State()
    select_date = State()
    select_time = State()
