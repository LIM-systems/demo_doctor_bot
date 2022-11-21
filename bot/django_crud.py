from asgiref.sync import sync_to_async
from records import models as mdl


@sync_to_async
def create_new_user(contact: dict):
    new_user = mdl.Clients.objects.get_or_create(
        tg_id=contact.get('user_id'),
        name=f"{contact.get('first_name')} {contact.get('last_name')}",
        phone=contact.get('phone_number').replace('+', ''),
    )
    print(new_user)
    return new_user


@sync_to_async
def create_new_record(record: dict):
    new_record = mdl.Records.objects.create(
        date=record.get('select_date'),
        time=record.get('select_time'),
        doctor_id=record.get('doctor_id'),
        user_id=record.get('client_id'),
    )
    print(new_record)
    new_record.save()
    return new_record


@sync_to_async
def delete_record_for_id(id):
    record = mdl.Records.objects.get(id=id)
    record.delete()
    print(record)
    return record


@sync_to_async()
def get_all_specials():
    '''Выбор всех специальностей'''
    all = mdl.Specials.objects.all()
    return [a for a in all]


@sync_to_async()
def get_doctor_special(specilas):
    '''Выбор врача по специальности'''
    select_doctor = mdl.Doctors.objects.filter(special__name=specilas)
    return [a for a in select_doctor]


@sync_to_async()
def get_doctor_detail(doctor):
    '''Просмотр подробностей о враче'''
    doctor_details = mdl.Doctors.objects.get(name=doctor)
    return doctor_details


@sync_to_async()
def get_client_for_tgid(tg_id):
    '''Получить клиент ID по tg_id'''
    client = mdl.Clients.objects.get(tg_id=tg_id)
    return client


@sync_to_async()
def get_doctor_for_name(special='', id=''):
    '''Получить доктор ID по name'''
    if special:
        doctor = mdl.Doctors.objects.get(id=id)
        return doctor.special
    if id:
        doctor = mdl.Doctors.objects.get(id=id)
        return doctor


@sync_to_async()
def my_records(tg_id):
    '''Получить записи к врачу по tg_id'''
    my_records = mdl.Records.objects.filter(user__tg_id=tg_id, finish=False).order_by('-date', '-time')
    return [a for a in my_records]