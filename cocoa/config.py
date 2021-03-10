import asyncio
from discord import User, Client, TextChannel

from model import ModelService


class ConfigService:
    def __init__(self, modelsvc: ModelService):
        self.modelsvc = modelsvc

    async def register_user(self, user: User, channel: TextChannel, client: Client):
        await channel.send('Tell me a little more about yourself!')

        try:
            description = await client.wait_for('message', timeout=300)
        except asyncio.TimeoutError:
            return await channel.send('Sorry, you took too long.. aborting setup')

        self.modelsvc.add_user(user.id, description)
        await channel.send("Awesome! Looks like we're good to go. Go ahead and schedule a session if you'd like")

    async def delete_user(self, user: User, channel: TextChannel):
        self.modelsvc.delete_user(user.id)
        await channel.send("Done! Sad to see you go :(")
