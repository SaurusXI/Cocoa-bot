from discord import Client, Message

from config import ConfigService
from scheduler import Scheduler


class Controller:
    def __init__(self, prefix: str, configsvc: ConfigService, scheduler: Scheduler):
        self.configsvc = configsvc
        self.schedulersvc = scheduler
        self.prefix = prefix

    async def handle_message(self, message: Message, client: Client):
        if message.author == client.user:
            return
        
        if not message.content.startswith(self.prefix):
            return

        _, _, command = message.content.partition(' ')
        command = command.lower()
        author, channel = message.author, message.channel

        # User registration and related commands
        if command == 'setup':
            self.configsvc.register_user(author, channel, client)
        elif command == 'delete me':
            self.configsvc.delete_user(author.id, channel)
        # Scheduling meetings and related commands
        elif command == 'schedule new':
            self.schedulersvc.schedule(author.id, channel, client),
        elif command == 'schedule cancel':
            self.schedulersvc.cancel(author.id, channel, client)
        elif command == 'list meetings':
            self.schedulersvc.list_booked_meetings(author.id, channel)
        else:
            await message.channel.send("Sorry, I'm not sure what you mean. Please use the help command for a list of commands you can use.")