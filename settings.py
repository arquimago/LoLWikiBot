import telebot
from decouple import config

TOKEN = config('TOKEN')
WIKI = "leagueoflegends"
BOT = telebot.TeleBot(TOKEN)
