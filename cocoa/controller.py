from discord import Client, Message

from cocoa.config import ConfigService
from cocoa.scheduler import Scheduler

from cocoa.helpers import envloader


class Controller:
    def __init__(self, configsvc: ConfigService, scheduler: Scheduler):
        self.configsvc = configsvc
        self.schedulersvc = scheduler
        self.prefix = envloader.config['prefix']

    async def handle_message(self, message: Message, client: Client):
        print(client, message)
        if message.author == client.user:
            return
        
        if not message.content.startswith(self.prefix):
            return

        _, _, command = message.content.partition(' ')
        command = command.lower()
        author, channel = message.author, message.channel

        # User registration and related commands
        if command == 'setup':
            await self.configsvc.config_user(author, channel, client)
        elif command == 'delete me':
            await self.configsvc.delete_user(author, channel)
        # Scheduling meetings and related commands
        elif command == 'schedule new':
            await self.schedulersvc.schedule(author.id, channel, client),
        elif command == 'schedule cancel':
            await self.schedulersvc.cancel(author.id, channel, client)
        elif command == 'list meetings':
            await self.schedulersvc.list_booked_meetings(author.id, channel)
        else:
            await message.channel.send("Sorry, I'm not sure what you mean. Please use the help command for a list of "
                                       "commands you can use.")