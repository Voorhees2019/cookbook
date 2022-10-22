from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Runs a telegram recipe bot"

    def handle(self, *args, **kwargs):
        from telegram_bot import bot
