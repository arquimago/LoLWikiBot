#!/usr/bin/python3
# -*- coding: utf-8 -*-

import fandom
import telebot
from settings import BOT, WIKI, LANGUAGE

fandom.set_lang(LANGUAGE) 
fandom.set_wiki(WIKI)
print("STARTANDO")

@BOT.message_handler(commands=['start','help', 'info'])
def send_welcome_start(message):
    BOT.reply_to(message, "Para utilizar esse bot apenas escreva " \
        "@lolwbot e os termos da busca, não envie a mensagem apenas " \
        "aguarde os resultados numa caixa popup")

@BOT.inline_handler(lambda query: query.query)
def query_text(inline_query):
    
    nada = telebot.types.InlineQueryResultArticle("0", "Nada encontrado", telebot.types.InputTextMessageContent("Não há nada sobre '"+ inline_query.query + "' no " + WIKI))
    try:
        search_results = fandom.search(inline_query.query)
        results = []
        
        for i, page_result in enumerate(search_results):
            
            page = fandom.page(page_result[0])
                
            title, url = page.title, page.url
            url = url.replace(' ', '%20')
            results.append(telebot.types.InlineQueryResultArticle(str(i), title, telebot.types.InputTextMessageContent(url)))

        if(len(results) == 0):
            results.append(nada)
        BOT.answer_inline_query(inline_query.id, results)
    except:
        BOT.answer_inline_query(inline_query.id, [nada])

print("CONFIGURADO")
BOT.polling(none_stop=True, interval=0, timeout=20)
