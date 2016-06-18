#!/usr/bin/python3
# -*- coding: utf-8 -*-

import wikia
import telebot

TOKEN = "YOUR TOKEN HERE"
WIKI = "leagueoflegends"
BOT = telebot.TeleBot(TOKEN)

@BOT.message_handler(commands=['start'])
def send_welcome_start(message):
    BOT.reply_to(message, "Testanto o PYTHON 3")

@BOT.message_handler(commands=['help'])
def send_welcome_help(message):
    BOT.reply_to(message, "Para utilizar esse bot apenas escreva " \
        "@lolwbot e os termos da busca, não envie a mensagem apenas " \
        "aguarde os resultados numa caixa popup")

@BOT.message_handler(commands=['info'])
def send_welcome_info(message):
    BOT.reply_to(message, "O propósito deste bot é apenas fazer buscas inline, "\
        "se deseja mais interações e informações sobre o jogo, campeões, " \
        "invocadores, partidas e tudo mais recomendo utilizar o " \
        "@League_of_Legends_bot criado pelo @Edurolp e com tradução para " \
        "Português feita por mim (@Arquimago).")

@BOT.inline_handler(lambda query: query.query)
def query_text(inline_query):
    total = 10
    try:
        search_results = wikia.search(WIKI, inline_query.query, total)
        results = []

        for i, page_result in enumerate(search_results):
            try:
                page = wikia.page(WIKI, page_result)
            except:
                break

            title, url = page.title, page.url
            url = url.replace(' ', '%20')
            results.append(telebot.types.InlineQueryResultArticle(str(i), title, url))

        BOT.answer_inline_query(inline_query.id, results)

    except Exception as ex:
        print(ex)

BOT.polling(none_stop=True, interval=0, timeout=20)
