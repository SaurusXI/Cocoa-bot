from discord import Client, Message

from config import ConfigService
from scheduler import Scheduler


class Controller:
    def __init__(self, prefix: str, configsvc: ConfigService, scheduler: Scheduler):
        self.configsvc = configsvc
        self.schedulersvc = scheduler
        self.prefix = prefix

    def handle_message(self, message: Message, client: Client):
        if message.author == client.user:
            return
        
        if not message.content.startswith(self.prefix):
            return

        _, _, command = message.content.partition(' ')
        author, channel = message.author, message.channel

        # User registration and related commands
        if command == 'setup':
            self.configsvc.register_user(author, channel, client)
        elif command == 'delete_me':
            self.schedulersvc.delete_user(author, channel)
        # Scheduling meetings and related commands
        elif command == 'schedule_new':
            self.schedulersvc.schedule(author.id)
        elif command == 'schedule_cancel':
            self.schedulersvc.cancel(author.id, channel, client)
        elif command == 'list_all_meetings':
            self.schedulersvc.list_booked_meetings(author.id, channel)
        else:
            await channel.send(
                "Wrong command."
            )