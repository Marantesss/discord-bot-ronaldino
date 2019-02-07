# This module contains a list of all commands the bot can respond to
# Please feel free to give sugestions as well as correct some stuff

import requests
import json

def hello_command(message, handler, args):
    try:
        return "Hello {}, have a wonderful day :ok_hand:".format(message.author.mention)
    except Exception as e:
        print(e)

def info_command(message, handler, args):
    try:
        msg = "Thank you {} for wanting to know more about me :yum:\n".format(message.author.mention)
        msg += "I am currently being built :tools: with much love by `Gonçalo \'Marantesss\' Marantes`, but I still have a long way to go!\n"
        msg += "If you happen to come accross any bugs :ant: or want a new feature to be implemented, please do say so! :desktop:"
        return msg
    except Exception as e:
        print(e)

def help_command(message, handler, args):
    try:
        count = 1
        coms = "**What can I do?**\n"
        for command in handler.commands:
            coms += "**{}.)** `{}` : {}\n".format(count, command['trigger'], command['description'])
            count += 1
        return coms
    except Exception as e:
        print(e)
    
def ip_command(message, handler, args):
    try:
        req = requests.get('http://ip-api.com/json/{}'.format(args[0]))
        resp = json.loads(req.content.decode())
        if req.status_code == 200:
            if resp['status'] == 'success':
                template = ':computer: **{}** :computer:\n**IP:** {}\n**Country:** {}\n**State:** {}\n**City:** {}\n**Latitude:** {}\n**Longitude:** {}\n**ISP:** {}\n**ORG:** {}\nImported from: `http://ip-api.com`'
                out = template.format(args[0], resp['query'], resp['country'], resp['regionName'], resp['city'], resp['lat'], resp['lon'], resp['isp'], resp["org"])
                return out
            elif resp['status'] == 'fail':
                return ':no_entry: **API Request Failed** :no_entry:'
        else:
            return ':no_entry: **HTTP Request Failed** :no_entry: : Error {}'.format(req.status_code)
    except Exception as e:
        print(e)

def weather_command(message, handler, args):
    try:
        return ":no_entry: Yikes :no_entry:\n:tools: `weather_command` is under construction :tools:"
    except Exception as e:
        print(e)
