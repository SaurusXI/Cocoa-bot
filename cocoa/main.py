import os

from yaml import load, Loader
import discord

# from cocoa import booking, config, notifier, scheduler, controller


config_path = os.path.join('..', 'config.yaml')

client = discord.Client()

with open(config_path, 'r') as f:
    config = load(f, Loader=Loader)


@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    # route stuff using controller
    pass


client.run('bot token here')