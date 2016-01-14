#!/usr/bin/env python3
#! encoding:utf-8

import telebot
import os
from telebot import types
import collections
import datetime
import requests

TOKEN = os.environ.get("TELEGRAM_TOKEN","") 
MEETUP_KEY = os.environ.get("MEETUP_KEY","")
group_name = 'GDG-Aracaju'

default_payload = { 'status': 'upcoming' }
bot = telebot.TeleBot(TOKEN)

def generate_events(group_name, api_key):
    offset = 0
    while True:
        offset_payload = { 'offset': offset,
                           'key': api_key,
                           'group_urlname': group_name }
        payload = default_payload.copy()
        payload = {**default_payload, **offset_payload}
        print(payload)

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
    print("olá")
    bot.reply_to(message, "Este bot faz buscas no Meetup do GDG Aracaju: http://meetup.com/GDG-Aracaju")

@bot.message_handler(commands=['events'])
def query_text(message):
    print("hello")
    try:
        all_events = list(generate_events(group_name, MEETUP_KEY))
        response = ""
        print(all_events)
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
