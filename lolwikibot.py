# coding: latin-1

import wikia
import telebot
from telebot import types
import requests

TOKEN = "YOUR TOKEN HERE"
wiki = "leagueoflegends"
bot = telebot.TeleBot(TOKEN)

teclado = types.ReplyKeyboardMarkup(resize_keyboard=True)
teclado.row('start')
teclado.row('help')
teclado.row('info')

@bot.message_handler(commands=['start'])
def send_welcome(message,reply_markup=teclado):
	bot.reply_to(message, "Este bot faz buscas inline na Wiki de League of Legends, feito por @Arquimago")
	
@bot.message_handler(commands=['help'])
def send_welcome(message,reply_markup=teclado):
	bot.reply_to(message, "Para utilizar esse bot apenas escreva @lolwbot e os termos da busca, não envie a mensagem apenas aguarde os resultados numa caixa popup")
	
@bot.message_handler(commands=['info'])
def send_welcome(message,reply_markup=teclado):
	bot.reply_to(message, "O propósito deste bot é apenas fazer buscas inline, se deseja mais interações e informações sobre o jogo, campeões, invocadores, partidas e tudo mais recomendo utilizar o @League_of_Legends_bot criado pelo @Edurolp e com tradução para Português feita por mim (@Arquimago).")

@bot.inline_handler(lambda query: query.query)
def query_text(inline_query):
	total = 10
	try:
		s = wikia.search(wiki,inline_query.query,total)
		results = range(0,total)
		
		for i in range(0,len(s)):
			try: 
				url = wikia.page(wiki,s[i]).url
			except:
				break
			url = url.replace(' ', '%20')
			title = wikia.page(wiki,s[i]).title
			id = "%d"%i
			results[i] = types.InlineQueryResultArticle(id, title, url)
		
		bot.answer_inline_query(inline_query.id, results)
		
	except Exception as e:
		print(e)

requests.packages.urllib3.disable_warnings()

bot.polling(none_stop=True, interval=0, timeout=20)
