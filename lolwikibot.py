import wikia
import telebot
from telebot import types

TOKEN = #INSIRA SEU TOKEN AQUI COMO STRING, ENTRE "ASPAS"
lol = "leagueoflegends"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Este bot faz buscas na Wiki de League of Legends")
	
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, "Este bot foi programado pra funcionar apenas em buscas em linha. Use sempre em um grupo. Feito por @Arquimago")

@bot.inline_handler(lambda query: query.query)
def query_text(inline_query):
	try:
		s = wikia.search(lol,inline_query.query)
        url1 = wikia.page(lol,s[0]).url
        url2 = wikia.page(lol,s[1]).url
		title1 = wikia.page(lol,s[0]).title
		title2 = wikia.page(lol,s[1]).title
        r = types.InlineQueryResultArticle('1', title1, url1)
        r2 = types.InlineQueryResultArticle('2', title2, url2)
        bot.answer_inline_query(inline_query.id, [r, r2])
    except Exception as e:
        print(e)

bot.polling()
