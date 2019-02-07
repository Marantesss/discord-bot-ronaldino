#
#   Name: discord-bot-ronaldino
#   Author: Goncalo "Marantesss" Marantes
#   Version: 1.0
#

# An API wrapper for Discord written in Python.
import discord
# A module containing a class for command handling
from command_handler import CommandHandler
# A module containing a list of all commands
import commands

# create discord client
client = discord.Client()

# bot token
token = "XXXXXX"

# create the CommandHandler object and pass it the client
ch = CommandHandler(client)

'''
Creating commands for the bot
'''

## help command
ch.add_command({
    "trigger": "+commands",
    "function": commands.help_command,
    "args_num": 0,
    "args_name": [],
    "description": "I will tell you everything I can do!"
})
## hello command
ch.add_command({
    "trigger": "+hello",
    "function": commands.hello_command,
    "args_num": 1,
    "args_name": ["string"],
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

# bot is ready
@client.event
async def on_ready():
    try:
        # print bot information
        print(client.user.name)
        print(client.user.id)
        print("Discord.py Version: {}".format(discord.__version__))
        await client.change_presence(game=discord.Game(name="Under construction"))
        
    except Exception as e:
        print(e)

# on new message
@client.event
async def on_message(message):
    # we do not want the bot to respond to itself, duh
    if message.author == client.user:
        return
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
client.run(token)
