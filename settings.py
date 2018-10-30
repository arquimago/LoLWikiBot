import logging
import telebot
from decouple import config

logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)

TOKEN = config('TOKEN')
WIKI = "leagueoflegends"
BOT = telebot.TeleBot(TOKEN)
