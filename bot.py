#
#   Name: discord-bot-ronaldino
#   Author: Goncalo "Marantesss" Marantes
#   Version: 1.0
#

import discord

# create discord client
client = discord.Client()

# bot token
token = "NTQyMDY2NjEwODc4MjgzODAw.Dzorpw.3RohsSVdbsKywlK4XXF2UOq2Yqg"

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
	# print message content
	# await message.content
    # we do not want the bot to respond to itself
    if message.author == client.user:
        return
    # Hello
    if message.content.startswith("+hello"):
        msg = "Hello {0.author.mention}".format(message)
        await client.send_message(message.channel, msg)
    # Information
    if message.content.startswith("+info"):
        msg = "Thank you {0.author.mention} for wanting to know more about me :yum:\n".format(message)
        msg += "I am currently being built with much love, but I still have a long way to go!\n"
        msg += "If you happen to come accross any bugs or want a new feature to be implemented, please do say so! :desktop:"
        await client.send_message(message.channel, msg)

# start bot
client.run(token)
