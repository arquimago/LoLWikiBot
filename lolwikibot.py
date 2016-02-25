# coding: latin-1

import wikia
import telebot
from telebot import types

TOKEN = "169600264:AAGp6eMUBEb96pe2yTGN-xkpw9hiJemSF6Y"
lol = "leagueoflegends"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "Este bot faz buscas na Wiki de League of Legends, feito por @Arquimago")

@bot.inline_handler(lambda query: query.query)
def query_text(inline_query):
	try:
		s = wikia.search(lol,inline_query.query,10)
		results = range(0,len(s))
		
		for i in range(0,len(s)):
		
			url = wikia.page(lol,s[i]).url
			url = url.replace(' ', '%20')
			title = wikia.page(lol,s[i]).title
			id = "%d"%i
			results[i] = types.InlineQueryResultArticle(id, title, url)
		
		bot.answer_inline_query(inline_query.id, results)
		
	except Exception as e:
		print(e)

bot.polling()
