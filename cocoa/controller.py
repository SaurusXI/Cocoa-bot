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

        if command == 'setup':
            self.configsvc.register_user(author, channel, client)
        elif command == 'schedule':
            self.schedulersvc.schedule(author.id)