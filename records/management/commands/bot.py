from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Телеграм ДокторБОТ'

    def handle(self, *args, **options):
        from aiogram import executor
        import bot.handlers
        from bot.loader import dp

        executor.start_polling(dp)
