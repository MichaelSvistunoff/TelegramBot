from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    ApplicationBuilder,
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)
import requests
import locale
import datetime
import emoji
from spy import *
from typing import Dict

locale.setlocale(locale.LC_ALL, 'ru_RU')

 
def calc_run(usrerexp):
    return eval(usrerexp)

# What can i do
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('<b>Что я умею:</b>\
        \n------------------------------\
        \n/hello\
        \n/fun\
        \n/new_year\
        \n/phrase', parse_mode='HTML')

# Hello, {User}
async def hello_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'{emoji.emojize(":waving_hand:")} Привет, <b>{update.effective_user.first_name}</b>!\
        \n------------------------------\
        \n{emoji.emojize(":calendar:")} Сегодня {datetime.datetime.now().strftime("%A, %d %B, %Y")}', parse_mode='HTML')

#Calc
async def calc_programm(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(calc_run(update.message.text.split(" ")[1]))

#Days to New Year
async def days_to_new_year(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:    
    now = datetime.datetime.today()
    new_year = datetime.datetime(now.year + 1, 1, 1)
    days_to_new_year = new_year - now
    mm, ss = divmod(days_to_new_year.seconds, 60)
    hh, mm = divmod(mm, 60)
    await update.message.reply_text('{} <b>До нового года осталось:</b>\
        \n------------------------------\
        Дней: {}, часов: {}; минут {}; секунд: {}'.format(emoji.emojize(":spiral_calendar:"), days_to_new_year.days, hh, mm, ss), parse_mode='HTML')
    
#Random phrase
async def random_phrase(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    url = 'http://api.forismatic.com/api/1.0/'
    payload  = {'method': 'getQuote', 'format': 'json', 'lang': 'ru'}
    res = requests.get(url, params=payload)
    data = res.json()    
    await update.message.reply_text('{} <b>Рандомная цитата:</b>\
        \n------------------------------\
        \n<i>{}</i>\
        \n------------------------------\
        \n{}'.format(emoji.emojize(":infinity:"), data['quoteText'], data['quoteAuthor']), parse_mode='HTML')