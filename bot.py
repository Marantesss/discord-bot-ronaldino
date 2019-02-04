import discord

# create discord client
client = discord.Client()

# bot token
token = "NTQyMDY2NjEwODc4MjgzODAw.Dzorpw.3RohsSVdbsKywlK4XXF2UOq2Yqg"

# bot is ready
@client.event
async def on_ready():
    try:
        # print bot infomration
        print(client.user.name)
        print(client.user.id)
        print("Discord.py Version: {}".format(discord.__version__))
        
    except Exception as e:
        print(e)

# on new message
@client.event
async def on_message(message):
	# print message content
	# await message.content
    # we do not want the bot to respond to itslef
    if message.author == client.user:
        return
    if message.content.startswith("+hello"):
        msg = "Hello {0.author.mention}".format(message)
        await client.send_message(message.channel, msg)

# start bot
client.run(token)
