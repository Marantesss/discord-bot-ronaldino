# This module contains a list of all commands the bot can respond to
# Please feel free to give sugestions as well as correct some stuff

import os
import json
from json.decoder import JSONDecodeError
# Allows to send http requests
import requests
# OpeanWeatherMap API written in python
from pyowm import OWM
# spotify API written in python
import spotipy
import spotipy.util as util
import ast

# getting top secret information
with open("settings.json") as settingsFile:
	settings = json.load(settingsFile)

# 'logging in' to spotify
try:
    username = settings["spotify_user_id"]
    if os.path.isfile(f".cache-{username}"):
        with open(f".cache-{username}") as cache:
            s = cache.read()
            token = s[18:164]
    else:
        token = util.prompt_for_user_token(username, None, settings["spotify_client_id"], settings["spotify_client_secret"], settings["spotify_redirect_uri"])
    spotify = spotipy.Spotify(auth=token)
except (AttributeError, JSONDecodeError):
        os.remove(f".cache-{username}")
        token = util.prompt_for_user_token(settings["spotify_user_id"], None, settings["spotify_client_id"], settings["spotify_client_secret"], settings["spotify_redirect_uri"])
        spotify = spotipy.Spotify(auth=token)

def hello_command(message, handler, args):
    try:
        return "Hello {}, have a wonderful day :ok_hand:".format(message.author.mention)
    except Exception as e:
        print(e)


def info_command(message, handler, args):
    try:
        msg = "Thank you {} for wanting to know more about me :yum:\n".format(message.author.mention)
        msg += "I am currently being built :tools: with much love by `Gonçalo \'Marantesss\' Marantes`, but I still have a long way to go!\n"
        msg += "If you happen to come accross any bugs :ant: or want a new feature to be implemented, please do say so! :desktop:\n"
        msg += "Take a look at my **source code:** https://github.com/Marantesss/discord-bot-ronaldino"
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
                template = ':computer: **{}** :computer:\n**IP:** {}\n**Country:** {}\n**State:** {}\n**City:** {}\n**Latitude:** {}\n**Longitude:** {}\n**ISP:** {}\n**ORG:** {}\nSource: `http://ip-api.com`'
                out = template.format(args[0], resp['query'], resp['country'], resp['regionName'], resp['city'], resp['lat'], resp['lon'], resp['isp'], resp["org"])
                return out
            elif resp['status'] == 'fail':
                return ':no_entry: **API Request Failed** :no_entry:'
        else:
            return ':no_entry: **HTTP Request Failed** :no_entry: : Error {}'.format(req.status_code)
    except Exception as e:
        print(e)


def dictionary_command(message, handler, args):
    try:
        app_id = settings["dic_app_id"]
        app_key = settings["dic_app_key"]
        language = 'en'
        word_id = args[0]
        url = 'https://od-api.oxforddictionaries.com:443/api/v1/entries/'  + language + '/'  + word_id.lower()
        #url Normalized frequency
        #urlFR = 'https://od-api.oxforddictionaries.com:443/api/v1/stats/frequency/word/'  + language + '/?corpus=nmc&lemma=' + word_id.lower()
        req = requests.get(url, headers = {'app_id' : app_id, 'app_key' : app_key})
        resp = json.loads(req.content)
        if req.status_code == 200:
            results = resp["results"]
            etymologies = results[0]["lexicalEntries"][0]["entries"][0]["etymologies"]
            definition = results[0]["lexicalEntries"][0]["entries"][0]["senses"][0]["definitions"]
            template = ':books: **{}** :books:\n**Definition:** {}\n**Etymologies:** {}\nSource: `https://od-api.oxforddictionaries.com`'
            out = template.format(word_id, definition, etymologies)
            return out
        else:
            return ':no_entry: **HTTP Request Failed** :no_entry: : Error {}'.format(req.status_code)
    except Exception as e:
        print(e)


def birthday_command(message, handler, args):
    try:
        with open("birthdays.json") as birthdaysFile:
	        birthdays = json.load(birthdaysFile)
        # checking if we want to see all birtdays
        msg = ":gift: **Birthdays** :birthday:\n"
        if args[0] == "all":
            for name, date in birthdays.items():
                msg += "**{0}:** :arrow_right: {1} de {4} - {1}/{2}/{3}\n".format(name, date[0], date[1], date[2], date[3])
            return msg
        elif args[0] in birthdays:
            date = birthdays[args[0]]
            msg += "**{0}:** :arrow_right: {1} de {4} - {1}/{2}/{3}".format(args[0], date[0], date[1], date[2], date[3])
            return msg
        else:
            return ":no_entry: **ERROR** :no_entry: : No info on {}'s birthday".format(args[0])
    except Exception as e:
        print(e)


def weather_command(message, handler, args):
    try:
        open_weather_map = OWM(settings["open_weather_key"])
        if  open_weather_map.is_API_online():
            # observation
            query = args[0] + ", " + args[1]
            obs = open_weather_map.weather_at_place(query)
            # weather
            weather = obs.get_weather()
            wind = weather.get_wind()
            temp = weather.get_temperature(unit="celsius")
            #location
            loc = obs.get_location()
            msg = ":partly_sunny: **Weather** :thunder_cloud_rain:\n"
            msg += "**City:** {}\t**Country:** {}\n**Latitude:** {}\t**Longitude:** {}\n**Status:** {}\n**Temperature** :thermometer:\n**Average:** {}ºC\t**Max:** {}ºC\t**Min:** {}ºC\n**Wind:** {}m/s"
            msg = msg.format(loc.get_name(), args[1].upper(), loc.get_lat(), loc.get_lon(), weather.get_detailed_status(), temp["temp"], temp["temp_max"], temp["temp_min"], wind["speed"])
            return msg
        else:
            return ":no_entry: **ERROR** :no_entry: : OpeanWeatherMap API is offline!"
    except Exception as e:
        print(e)

def spotify_command(message, handler, args):
    try:
        # getting the full search string and search results
        searchResults = spotify.search(" ".join(args),1,0,"artist")
        # getting info from JSON file
        artistInfo = searchResults["artists"]["items"][0]
        msg = ":musical_note: **Artist** :microphone:\n"
        msg += "**Name:** {}\n**Genres:** {}\n**Followers:** {}\n**Image:** {}".format(artistInfo["name"], artistInfo["genres"], artistInfo["followers"]["total"], artistInfo["images"][0]["url"])
        return msg
    except Exception as e:
        print(e)
