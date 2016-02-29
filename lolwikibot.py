# coding: latin-1

import wikia
import telebot
import ConfigParser
from telebot import types

config = ConfigParser.RawConfigParser()
config.read('config.ini')

TOKEN = config.get('bot father', 'token')
wiki_name = config.get('wikia', 'wiki_name')
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
	bot.reply_to(message, "Este bot faz buscas inline na Wiki de League of Legends, feito por @Arquimago")
	
@bot.message_handler(commands=['help'])
def send_welcome(message):
	bot.reply_to(message, "Para utilizar esse bot apenas escreva @lolwbot e os termos da busca, não envie a mensagem apenas aguarde os resultados numa caixa popup")
	
@bot.message_handler(commands=['info'])
def send_welcome(message):
	bot.reply_to(message, "O propósito deste bot é apenas fazer buscas inline, se deseja mais interações e informações sobre o jogo, campeões, invocadores, partidas e tudo mais recomendo utilizar o @League_of_Legends_bot criado pelo @Edurolp e com tradução para Português feita por mim (@Arquimago).")

@bot.inline_handler(lambda query: query.query)
def query_text(inline_query):
	total_de_resultados = 30
	erro_wiki = "The Journal of Justice:"
	try:
		s = wikia.search(wiki_name,inline_query.query,total_de_resultados)
		resultados = range(0,len(s))
		
		for i in range(0,len(s)):
			erro = s[i].find(erro_wiki)
			if(erro>-1):
				break
			url = wikia.page(wiki_name,s[i]).url
			url = url.replace(' ', '%20')
			title = wikia.page(wiki_name,s[i]).title
			id = "%d"%i
			resultados[i] = types.InlineQueryResultArticle(id, title, url)
		
		bot.answer_inline_query(inline_query.id, resultados)
		
	except Exception as e:
		print(e)

bot.polling(none_stop=True, interval=0, timeout=20)
