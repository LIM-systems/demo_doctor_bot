from django.contrib.auth.models import AbstractUser
from django.db import models


class Users(AbstractUser):
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=200,
    )
    phone = models.CharField(
        verbose_name='Телефон',
        max_length=12,
        blank=False
    )

    # REQUIRED_FIELDS = ('username',)

    def __str__(self):
        return self.username


class Clients(models.Model):
    tg_id = models.BigIntegerField(
        verbose_name='Telegram ID',
        help_text='Telegram ID для записи через бот и оповещения',
        blank=False,
        default=0)
    name = models.CharField(
        verbose_name='Имя',
        help_text='Имя клиента',
        max_length=200,
    )
    phone = models.CharField(
        verbose_name='Телефон',
        help_text='Телефон клиента',
        max_length=15,
    )
    # photo = models.ImageField(
    #     verbose_name='Фото клиента',
    #     upload_to='photo_client/',
    #     blank=True)

    class Meta:
        verbose_name = 'Клинта'
        verbose_name_plural = 'Клиент'

    def __str__(self):
        return self.name


class Specials(models.Model):
    name = models.CharField(
        verbose_name='Название специальности',
        help_text='Укажите название специальности',
        unique=True,
        max_length=200,
        default=''
    )

    class Meta:
        verbose_name = 'Специальности'
        verbose_name_plural = 'Специальность врача'

    def __str__(self):
        return self.name


class Doctors(models.Model):
    name = models.CharField(
        verbose_name='Имя врача',
        max_length=200,
        blank=False)
    age = models.IntegerField(
        verbose_name='Возраст',
        blank=False
    )
    experiens = models.IntegerField(
        verbose_name='Опыт работы',
        help_text='Стаж в годах',
        blank=False
    )
    achiv_short = models.CharField(
        max_length=255,
        verbose_name='Основные достижения',
        help_text='Выдаются в боте при выборе врача',
        blank=False
    )
    achiv = models.TextField(
        max_length=1000,
        verbose_name='Достижения и образование',
        help_text='Выдаются в боте при просмотре информации о враче',
        blank=False
    )
    email = models.EmailField(
        verbose_name='Почта врача',
        help_text='Почта для оповещения о записи клиентов',
        blank=False
    )
    special = models.ForeignKey(Specials, on_delete=models.PROTECT,
                                verbose_name='Специальность')
    photo = models.ImageField(
        verbose_name='Фото врача',
        upload_to='photo_doctor/',
        blank=False)

    class Meta:
        verbose_name = 'Врача'
        verbose_name_plural = 'Врачи'

    def __str__(self):
        return self.name


class Records(models.Model):
    user = models.ForeignKey(Clients, on_delete=models.DO_NOTHING,
                             verbose_name='Клиент')
    doctor = models.ForeignKey(Doctors, on_delete=models.DO_NOTHING,
                               verbose_name='Врач')
    date = models.DateField(
        verbose_name='Дата посещения',
        blank=False)
    time = models.TimeField(
        verbose_name='Время посещения',
        blank=False)
    finish = models.BooleanField(
        verbose_name='Прием окончен',
        help_text='Запланирован или закончен примем клиента',
        default=False
    )

    def __str__(self):
        return f'Запись к врачу'

    class Meta:
        verbose_name = 'Запись'
        verbose_name_plural = 'Журнал записей'
