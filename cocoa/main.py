import cocoa

from yaml import load, Loader
import discord

from cocoa.helpers import envloader

# from cocoa import booking, config, notifier, scheduler, controller

client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    # route stuff using controller
    pass


client.run(envloader.config['bot_token'])