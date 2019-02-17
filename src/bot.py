#
#   Name: discord-bot-ronaldino
#   Author: Goncalo "Marantesss" Marantes
#   Version: 0.2.1
#

import json
# An API wrapper for Discord written in Python.
import discord
# A module containing a class for command handling
from command_handler import CommandHandler
# A module containing a list of all commands
import commands

# getting top secret information
with open("settings.json") as settingsFile:
	settings = json.load(settingsFile)

# create discord bot client
ronaldino = discord.Client()

# bot token
token = settings["bot_token"]

# create the CommandHandler object and pass it the client
ch = CommandHandler(ronaldino)

'''
Creating commands for the bot
'''
## help command
ch.add_command({
    "trigger": "+help",
    "function": commands.help_command,
    "args_num": 0,
    "args_name": [],
    "description": "I will tell you everything I can do!"
})
## hello command
ch.add_command({
    "trigger": "+hello",
    "function": commands.hello_command,
    "args_num": 0,
    "args_name": [],
    "description": "I will respond hello right back at ya!"
})
## info command
ch.add_command({
    "trigger": "+info",
    "function": commands.info_command,
    "args_num": 0,
    "args_name": [],
    "description": "I will tell you more about myself and the wonderful life of a bot!"
})
## ip command
ch.add_command({
    "trigger": "+ip",
    "function": commands.ip_command,
    "args_num": 1,
    "args_name": ["IP/Domain"],
    "description": "Feel like a hacker? I will tell you everything I can about an IP address!"
})
## dictionary command
ch.add_command({
    "trigger": "+dictionary",
    "function": commands.dictionary_command,
    "args_num": 1,
    "args_name": ["Word"],
    "description": "Want to know the meaing of a word? Give this command a try and let me enlighten you!"
})
## birthday command
ch.add_command({
    "trigger": "+birthday",
    "function": commands.birthday_command,
    "args_num": 1,
    "args_name": ["Birthday boy's name or 'all'"],
    "description": "Never forget your friends' birthday!"
})
## weather command
ch.add_command({
    "trigger": "+weather",
    "function": commands.weather_command,
    "args_num": 2,
    "args_name": ["City", "Country Code"],
    "description": "Oh crap, is it raining outside? Why bother looking out the window when you can simply ask me!"
})
## spotify command
ch.add_command({
    "trigger": "+spotify",
    "function": commands.spotify_command,
    "args_num": 1,
    "args_name": ["Search Query"],
    "description": "How about some music baby?"
})


# bot is ready
@ronaldino.event
async def on_ready():
    try:
        # print bot information
        print(ronaldino.user.name)
        print(ronaldino.user.id)
        print("Discord.py Version: {}".format(discord.__version__))
        await ronaldino.change_presence(game=discord.Game(name="Under construction"))
        
    except Exception as e:
        print(e)

# on new message
@ronaldino.event
async def on_message(message):
    # we do not want the bot to respond to itself, duh
    if message.author == ronaldino.user:
        await ronaldino.add_reaction(message, "\U0001F44C")
    # but we do want it to respond to other clients
    else:
        # looking for a command trigger
        try:
            await ch.command_handler(message)
        # message does not contain a trigger
        except TypeError:
            # do nothing
            pass
        # generic Python error
        except Exception as e:
            print(e)
        
# start bot
ronaldino.run(token)
