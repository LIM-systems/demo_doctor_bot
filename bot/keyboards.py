from aiogram import types


def menu_keyboard(array: list, row_width=2, one_time=False):
    '''Обычные кнопки для меню
    Принимает список, возвращает кнопки'''
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True,
                                       row_width=row_width,
                                       one_time_keyboard=one_time)
    markup.add(*array)
    return markup


def remove_keyboard():
    types.ReplyKeyboardMarkup()
    types.ReplyKeyboardRemove()


def inline_btns(array: list, call, emoji=''):
    '''Inline кнопки
    Принимает текст кнопок списком, callback.
    Возвращает кнопки'''
    markup = types.InlineKeyboardMarkup(row_width=3)
    for text in array:
        button = types.InlineKeyboardButton(text=f'{emoji}{text}',
                                            callback_data=f'{call}/{text}')
        markup.add(button)
    return markup


def get_contact():
    '''Кнопка для получения контакта'''
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    contact = types.KeyboardButton('📞 Передать телефон', request_contact=True)
    markup.add(contact)
    return markup