from datetime import datetime

from aiogram import types, executor
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from records import models
from bot.loader import dp, main_menu, app_docs, back, cancel
from bot import django_crud as dj, texts
from bot import keyboards as kb, states
from asgiref.sync import sync_to_async, async_to_sync
import asyncio
from pathlib import Path
import aiogram_calendar as calend


@dp.message_handler(commands=['start'])
async def start(msg: types.Message):
    '''Точка входа, регистрация или выдача меню'''
    name = msg.from_user.full_name
    await msg.answer(f'Мы рады тебя видеть {name}!')
    await asyncio.sleep(1)
    await msg.answer(texts.welcome,
                     reply_markup=kb.menu_keyboard(main_menu))


@dp.message_handler(Text(equals=main_menu[0]))
async def doctors_app(msg: types.Message):
    '''Выдаем все специальности'''
    specials = await dj.get_all_specials()
    await msg.answer(f'Выберите направление',
                     reply_markup=kb.inline_btns(specials, 'specials', '▫ '))


@dp.callback_query_handler(Text(startswith='specials'))
async def doctors_select_specials(call: types.CallbackQuery):
    '''Получаем название специальности, выдаем врачей этой специальности'''
    specials = call.data.split('/')[-1]
    get_specials = await dj.get_doctor_special(specials) + [back]
    await call.message.edit_text(
        f'Выберите врача {specials}',
        reply_markup=kb.inline_btns(get_specials, f'get_doc/{specials}'))


@dp.callback_query_handler(Text(startswith='get_doc'))
async def doctor_details(call: types.CallbackQuery, state: FSMContext):
    '''Выдать анкету врача или Назад к списку специальностей
    call.data = get_doc/Терапевт/Имя врача'''
    btn = call.data.split('/')[-1]
    special = call.data.split('/')[1]
    if btn == back:
        specials = await dj.get_all_specials()
        await call.message.edit_text(
            f'Выберите направление',
            reply_markup=kb.inline_btns(specials, 'specials', '▫ '))
    else:
        doctors_details = await dj.get_doctor_detail(btn)
        photo = doctors_details.photo
        describe = f'''<b>{doctors_details.name}  {doctors_details.achiv_short}</b>
<b>Возраст:</b> {doctors_details.age}
<b>Опыт:</b> {doctors_details.experiens}
<b>Образование:</b> {doctors_details.achiv}'''
        await call.message.delete()
        with open(f'{Path().absolute()}/media/{photo}', 'rb') as doctor_photo:
            await call.message.answer_photo(doctor_photo,
                                            caption=describe,
                                            reply_markup=kb.inline_btns(app_docs, f'app/{special}'))
        await state.update_data(special=special)
        await state.update_data(doctor=doctors_details.name)
        await state.update_data(doctor_id=doctors_details.id)


@dp.callback_query_handler(Text(startswith='app'))
async def app_doc(call: types.CallbackQuery):
    '''Выдаем календарь или Назад к выбору специальностей
    call.data = app/Терапевт/🌀 Записаться на прием'''
    btn = call.data.split('/')[-1]
    special = call.data.split('/')[1]
    if btn == app_docs[1]:
        await call.message.delete()
        get_specials = await dj.get_doctor_special(special) + [back]
        await call.message.answer(f'Выберите врача {special}',
                                reply_markup=kb.inline_btns(get_specials, f'get_doc/{special}'))
    else:
        await call.message.answer('<b>Выберите дату визита к специалисту</b>',
                                  reply_markup=await calend.SimpleCalendar().start_calendar())


@dp.callback_query_handler(calend.simple_cal_callback.filter())
async def process_simple_calendar(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    '''Выдаем время записи к врачу'''
    start_day = 10  # начало рабочего дня
    end_day = 19  # конец рабочего дня

    selected, date = await calend.SimpleCalendar().process_selection(call, callback_data)
    if not date:
        return
    hour_now = datetime.now().hour
    day_now = datetime.now().day
    day_now_calendar = int(date.strftime("%d"))
    if hour_now > start_day and day_now_calendar == day_now:
        start_day = hour_now + 1  # уберем прошедшие часы
    if hour_now+1 >= end_day and day_now_calendar == day_now:
        await call.message.answer('<b>К сожалению на сегодня прием окончен. Выберите другую дату</b>')
        return
    if selected:
        date_str = date.strftime("%Y-%m-%d")
        await call.message.answer(
            f'<b>Вы выбрали дату:</b> {date_str}\n\n<b>Выберите время</b>',
            reply_markup=kb.inline_btns(
                [f'{x}:00' for x in range(start_day, end_day)], f'write')
        )
        await state.update_data(select_date=date_str)
        await call.message.delete()


@dp.callback_query_handler(Text(startswith='write/'))
async def get_time(call: types.CallbackQuery, state: FSMContext):
    '''Получаем время, запрашиваем номер телефона'''
    time_visit = call.data.split('/')[-1]
    await call.message.answer(
        'Передайте номер телефона для оформления заказа.\n<b>Нажмите кнопку ниже</b>',
        reply_markup=kb.get_contact())
    await state.update_data(select_time=time_visit)
    await call.message.delete()


@dp.message_handler(content_types=['contact'])
async def get_phone(msg: types.Message, state: FSMContext):
    '''{"phone_number": "+79651875659", "first_name": "Артём", "last_name": "Земцов #1ЛП", "user_id": 5341187651}'''
    await msg.delete()
    states = await state.get_data()
    get_or_create_user = await dj.create_new_user(dict(msg.contact))
    client = await dj.get_client_for_tgid(msg.from_id)
    states.update({'client_id': client.id})
    await dj.create_new_record(states)
    await msg.answer(f'''Вы успешно записаны на прием:
<b>{states.get('special')}
{states.get('doctor')}
{states.get('select_date')} {states.get('select_time')}</b>

Мы напомним Вам о визите!
Спасибо что вы с нами!''', reply_markup=kb.menu_keyboard(main_menu))
    await asyncio.sleep(10)
    with open('./media/doctor.png', 'rb') as pic:
        await msg.answer_photo(pic, caption=f'''<em>Демонстрация напоминания о приеме к врачу!</em>
Вы записаны на {states.get('select_date')} {states.get('select_time')}
<b>{states.get('special')}
{states.get('doctor')}</b>''')


@dp.message_handler(Text(equals=main_menu[1]))
async def about(msg: types.Message):
    with open(f'{Path().absolute()}/media/about.jpg', 'rb') as about:
        await msg.answer_photo(about, caption=texts.about)


@dp.message_handler(Text(equals=main_menu[2]))
async def my_records(msg: types.Message):
    my_rec = await dj.my_records(msg.from_id)
    if not my_rec:
        await msg.answer(f'Запланированных визитов не найдено')
        return

    for rec in my_rec:
        my_record = f'''Запланированный визит:
<b>{rec.date} {rec.time}
{await dj.get_doctor_for_name(special=True, id=rec.doctor_id)}
{await dj.get_doctor_for_name(id=rec.doctor_id)}</b>'''
        await msg.answer(
            my_record,
            reply_markup=kb.inline_btns((cancel,), f'_cancel/{rec.id}'))


@dp.callback_query_handler(Text(startswith='_cancel/'))
async def visit_cancel(call: types.CallbackQuery):
    '''Отмена записи'''
    visit_id = call.data.split('/')[1]
    await dj.delete_record_for_id(visit_id)
    await call.message.edit_text(f'Ваша запись отменена')
