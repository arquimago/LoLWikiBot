# coding: latin-1

import wikia
import telebot
from telebot import types

TOKEN = "INSIRA SEU TOKEN AQUI"
lol = "leagueoflegends"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "Este bot faz buscas na Wiki de League of Legends, feito por @Arquimago")

@bot.inline_handler(lambda query: query.query)
def query_text(inline_query):
	try:
		s = wikia.search(lol,inline_query.query)
		url1 = wikia.page(lol,s[0]).url
		url1 = url1.replace(' ', '%20')
		url2 = wikia.page(lol,s[1]).url
		url2 = url2.replace(' ', '%20')
		title1 = wikia.page(lol,s[0]).title
		title2 = wikia.page(lol,s[1]).title
		r = types.InlineQueryResultArticle('1', title1, url1)
		r2 = types.InlineQueryResultArticle('2', title2, url2)
		bot.answer_inline_query(inline_query.id, [r, r2])
#		resultado=[]
#		contador=0
#		for results in s:
#			print(result.title)
#			url = wikia.page(lol,s[contador]).url
#			url = url.replace(' ','%20')
#			title = wikia.page(lol,s[contador]).url
#			contador += 1
#			resultado+=types.InlineQueryResultArticle(contador,title,url)
#		bot.answer_inline_query(inline_query.id, resultado)
	except Exception as e:
		print("Olha o erro...")

bot.polling()
