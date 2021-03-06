import asyncio
from discord import User, Client, TextChannel

from cocoa.model import ModelService


class ConfigService:
    def __init__(self, modelsvc: ModelService):
        self.modelsvc = modelsvc

    async def config_user(self, user: User, channel: TextChannel, client: Client):
        if not self.modelsvc.read_user(user.id):
            await self.register_user(user, channel, client)
        else:
            await self.modify_user(user, channel, client)

    async def register_user(self, user: User, channel: TextChannel, client: Client):
        await channel.send('What should I call you?')
        try:
            username = await client.wait_for('message', timeout=300)
        except asyncio.TimeoutError:
            return await channel.send('Sorry, you took too long.. aborting setup')

        await channel.send(f'Hi {username.content}! Tell me more about yourself')
        try:
            description = await client.wait_for('message', timeout=300)
        except asyncio.TimeoutError:
            return await channel.send('Sorry, you took too long.. aborting setup')

        print(type(user.id))
        print(type(description.content))
        self.modelsvc.add_user(user.id, username.content, description.content)
        await channel.send("Awesome! Looks like we're good to go. Go ahead and schedule a session if you'd like")

    async def modify_user(self, user: User, channel: TextChannel, client: Client):
        await channel.send('Make changes to your description')

        try:
            updated_description = await client.wait_for('message', timeout=300)
        except asyncio.TimeoutError:
            return await channel.send('Took too long, unable to update description')

        self.modelsvc.update_user(user.id, updated_description.content)
        await channel.send("User {}, your description has been updated !".format(user.id))

    async def delete_user(self, user: User, channel: TextChannel):
        self.modelsvc.delete_user(user.id)
        await channel.send("Done! Sad to see you go :(")
