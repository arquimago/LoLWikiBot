# coding: latin-1

import wikia
import telebot
from telebot import types

TOKEN = "SEU TOKEN AQUI"
lol = "leagueoflegends"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "Este bot faz buscas na Wiki de League of Legends, feito por @Arquimago")

@bot.inline_handler(lambda query: query.query)
def query_text(inline_query):
	total_de_resultados = 30
	erro_lol = "The Journal of Justice:"
	try:
		s = wikia.search(lol,inline_query.query,total_de_resultados)
		resultados = range(0,len(s))
		
		for i in range(0,len(s)):
			erro = s[i].find(erro_lol)
			if(erro>-1):
				break
			url = wikia.page(lol,s[i]).url
			url = url.replace(' ', '%20')
			title = wikia.page(lol,s[i]).title
			id = "%d"%i
			resultados[i] = types.InlineQueryResultArticle(id, title, url)
		
		bot.answer_inline_query(inline_query.id, resultados)
		
	except Exception as e:
		print(e)

bot.polling(none_stop=True, interval=0, timeout=20)
