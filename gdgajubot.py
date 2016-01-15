#!/usr/bin/env python3
#! encoding:utf-8
import argparse
import logging
import telebot
import os
import collections
import datetime
import requests

# Configuring log
logging.basicConfig(level=logging.INFO)

# Configuring parameters
logging.info("Configurando parâmetros")
defaults = {
    'telegram_token': '',
    'meetup_key': '',
    'group_name': ''
}
parser = argparse.ArgumentParser(description='Bot do GDG Aracaju')
parser.add_argument('-t', '--telegram_token', help='Token da API do Telegram')
parser.add_argument('-m', '--meetup_key', help='Key da API do Meetup')
parser.add_argument('-g', '--group_name', help='Grupo do Meetup')
namespace = parser.parse_args()
command_line_args = {k:v for k, v in vars(namespace).items() if v}

_config = collections.ChainMap(command_line_args, os.environ, defaults)

# Starting bot
logging.info("Iniciando bot")
logging.info("Usando telegram_token=%s" % (_config["telegram_token"]))
logging.info("Usando meetup_key=%s" % (_config["meetup_key"]))
bot = telebot.TeleBot(_config["telegram_token"])

def generate_events():
    default_payload = { 'status': 'upcoming' }
    offset = 0
    while True:
        offset_payload = { 'offset': offset,
                           'key': _config["meetup_key"],
                           'group_urlname': _config["group_name"] }
        payload = default_payload.copy()
        payload.update(offset_payload)
        # Above is the equivalent of jQuery.extend()
        # for Python 3.5: payload = {**default_payload, **offset_payload}
        
        r = requests.get('https://api.meetup.com/2/events', params=payload)
        json = r.json()

        results, meta = json['results'], json['meta']
        for item in results:
            yield item

        # if we no longer have more results pages, stop…
        if not meta['next']:
            return

        offset = offset + 1

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    logging.info("/start")
    bot.reply_to(message, "Este bot faz buscas no Meetup do GDG Aracaju: http://meetup.com/GDG-Aracaju")

@bot.message_handler(commands=['events'])
def list_upcoming_events(message):
    logging.info("/events")
    try:
        all_events = list(generate_events())
        response = ""
        for event in all_events:
            # convert time returned by Meetup API
            time = int(event['time'])/1000
            time_obj = datetime.datetime.fromtimestamp(time)

            # create a pretty-looking date
            date_pretty = time_obj.strftime('%d/%m')
            
            event['date_pretty'] = date_pretty
            response = response + ("%s: %s %s \n" % (event["name"], event["date_pretty"], event["event_url"]))

        bot.reply_to(message, response)
    except Exception as e:
        print(e)

bot.polling()
