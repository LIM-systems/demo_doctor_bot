# Generated by Django 4.1.3 on 2022-11-18 09:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('records', '0004_doctors_achiv_short_alter_clients_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='clients',
            name='photo',
            field=models.ImageField(blank=True, upload_to='photo_client/', verbose_name='Фото клиента'),
        ),
        migrations.AlterField(
            model_name='doctors',
            name='photo',
            field=models.ImageField(upload_to='photo_doctor/', verbose_name='Фото врача'),
        ),
    ]