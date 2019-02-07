# This module contains a list of all commands the bot can respond to
# Please feel free to give sugestions as well as correct some stuff

import requests
import json

def hello_command(message, client, args):
    try:
        return "Hello {0.author.mention}, Argument One: {}".format(message.author, args[0])
    except Exception as e:
        return e

def info_command(message, client, args):
    try:
        msg = "Thank you {0.author.mention} for wanting to know more about me :yum:\n".format(message)
        msg += "I am currently being built with much love by `Gonçalo \'Marantesss\' Marantes`, but I still have a long way to go!\n"
        msg += "If you happen to come accross any bugs or want a new feature to be implemented, please do say so! :desktop:"
        return msg
    except Exception as e:
        return e

def help_command(message, client, args):
    try:
        count = 1
        coms = "**What can I do?**\n"
        for command in client.commands:
            coms += "**{}.)** `{}` : {}\n".format(count, command['trigger'], command['description'])
            count += 1
        return coms
    except Exception as e:
        print(e)
    
def ip_command(message, client, args):
    try:
        req = requests.get('http://ip-api.com/json/{}'.format(args[0]))
        resp = json.loads(req.content.decode())
        if req.status_code == 200:
            if resp['status'] == 'success':
                template = '**{}**\n**IP: **{}\n**City: **{}\n**State: **{}\n**Country: **{}\n**Latitude: **{}\n**Longitude: **{}\n**ISP: **{}'
                out = template.format(args[0], resp['query'], resp['city'], resp['regionName'], resp['country'], resp['lat'], resp['lon'], resp['isp'])
                return out
            elif resp['status'] == 'fail':
                return 'API Request Failed'
        else:
            return 'HTTP Request Failed: Error {}'.format(req.status_code)
    except Exception as e:
        print(e)
