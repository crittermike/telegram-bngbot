#!/usr/bin/env python
# -*- coding: utf-8 -*-
from uuid import uuid4
import re
from telegram import InlineQueryResultArticle, ParseMode, InputTextMessageContent
from telegram.ext import Updater, InlineQueryHandler, CommandHandler
import requests

def start(bot, update):
    update.message.reply_text('Use this as an inline bot while chatting with your friends by typing "@bngbot search query".')

def inlinequery(bot, update):
    query = update.inline_query.query
    results = list()
    
    headers = {'Ocp-Apim-Subscription-Key': '8be99a81965f4648b34ceab3c487f073'}
    params = {'q': query, 'mkt': 'en-us'};
    response = requests.get('https://api.cognitive.microsoft.com/bing/v7.0/search', params=params, headers=headers).json()
    if 'webPages' in response:
        for result in response['webPages']['value']:
            results.append(InlineQueryResultArticle(id=uuid4(),
                                                    title=result['name'],
                                                    input_message_content=InputTextMessageContent(result['url']),
                                                    hide_url=False,
                                                    description=result['snippet'],
                                                    thumb_width=32,
                                                    thumb_height=32,
						    thumb_url="https://i.imgur.com/B0peDpB.jpg",
                                                    url=result['url']))
    update.inline_query.answer(results)

def main():
    updater = Updater("384318849:AAHHyqcGIOJCl00IFcX9xmJU5oRytfrKLW4")
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(InlineQueryHandler(inlinequery))
    updater.start_polling()

    # Block until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()
