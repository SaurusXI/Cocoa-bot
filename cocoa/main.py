import discord
from dotenv import dotenv_values

from cocoa import booking, config, notifier, scheduler, controller


env_path = 'ENV_PATH_HERE'

client = discord.Client()

config = dotenv_values(env_path)


@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    # route stuff using controller
    pass


client.run('bot token here')