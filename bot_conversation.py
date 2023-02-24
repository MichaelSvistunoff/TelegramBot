from typing import Dict

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)
import requests, json
import emoji
    
CHOOSING, TYPING_REPLY, TYPING_CHOICE = range(3)

reply_keyboard = [
    ["Погода в городе", "Готово"],
]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)


def facts_to_str(user_data: Dict[str, str]) -> str:
    """Helper function for formatting the gathered user info."""
    facts = [f"{key} - {value}" for key, value in user_data.items()]
    return "\n".join(facts).join(["\n", "\n"])

#Начало диалога
async def fun(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        f'{emoji.emojize(":keyboard:")} Напиши название любого города, о погоде в котором ты бы хотел узнать больше'
    )

    return TYPING_CHOICE

#Получение инфы о погоде
async def regular_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:  
    search_city_name = update.message.text
    context.user_data["choice"] = search_city_name
    
    api_key = "5eb92095c4479e6fb837c51ef7055605"
    url = "https://api.openweathermap.org/data/2.5/weather?q=%s&appid=%s&units=metric&lang=ru" % (search_city_name, api_key)

    response = requests.get(url)
    data = json.loads(response.text)
    city_name = data["name"]
    country_name = data["sys"]["country"]
    current_temp = data["main"]["temp"]
    feels_like = data["main"]["feels_like"]
    weather_descr = data["weather"][0]["description"].title() 
    if current_temp < -14:
        await update.message.reply_text(f'{emoji.emojize(":globe_showing_Europe-Africa:")} <b>{city_name}, {country_name}</b>\
            \n------------------------------\
            \n{emoji.emojize(":thermometer:")} Температура составляет: <u>{current_temp}</u> градусов (ощуается как <u>{feels_like}</u> градусов)\
            \n{emoji.emojize(":magnifying_glass_tilted_left:")} {weather_descr.title() }\
            \n{emoji.emojize(":cold_face:")} <i>Лучше сегодня остаться дома и заняться домашними делами</i>\
            \n------------------------------\
            \nДля выхода из режима просмотра введи <b>Готово</b> и отправь', parse_mode='HTML')
    elif current_temp < 10:
        await update.message.reply_text(f'{emoji.emojize(":globe_showing_Europe-Africa:")} <b>{city_name}, {country_name}</b>\
            \n------------------------------\
            \n{emoji.emojize(":thermometer:")} Температура составляет: <u>{current_temp}</u> градусов (ощуается как <u>{feels_like}</u> градусов)\
            \n{emoji.emojize(":magnifying_glass_tilted_left:")} {weather_descr.title() }\
            \n{emoji.emojize(":smiling_face_with_heart-eyes:")} <i>Дела сами себя не сделают! Собирайся скорее на подвиги!</i>\
            \n------------------------------\
            \nДля выхода из режима просмотра введи <b>Готово</b> и отправь', parse_mode='HTML')
    elif current_temp > 10:
        await update.message.reply_text(f'{emoji.emojize(":globe_showing_Europe-Africa:")} <b>{city_name}, {country_name}</b>\
            \n------------------------------\
            \n{emoji.emojize(":thermometer:")} Температура составляет: <u>{current_temp}</u> градусов (ощуается как <u>{feels_like}</u> градусов)\
            \n{emoji.emojize(":magnifying_glass_tilted_left:")} {weather_descr.title() }\
            \n{emoji.emojize(":hot_face:")} <i>Летная погода для сворачивания гор!</i>\
            \n------------------------------\
            \nДля выхода из режима просмотра введи <b>Готово</b> и отправь', parse_mode='HTML')
    
    return TYPING_REPLY

#Введи название для поиска
async def custom_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        f'{emoji.emojize(":keyboard:")} Напиши название любого города, о погоде в котором ты бы хотел узнать больше'
    )

    return TYPING_CHOICE

#Хз, что это?
async def received_information(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Store info provided by user and ask for the next category."""
    user_data = context.user_data
    text = update.message.text
    category = user_data["choice"]
    user_data[category] = text
    del user_data["choice"]

    await update.message.reply_text(
        "Neat! Just so you know, this is what you already told me:"
        f"{facts_to_str(user_data)}You can tell me more, or change your opinion"
        " on something.",
        reply_markup=markup,
    )

    return CHOOSING

#Завершение диалога
async def done(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_data = context.user_data
    if "choice" in user_data:
        del user_data["choice"]

    await update.message.reply_text(
        f'{emoji.emojize(":red_heart:")} Спасибо за проявленный интерес!\nДо скорых встреч!',
        reply_markup=ReplyKeyboardRemove(),
    )

    user_data.clear()
    return ConversationHandler.END

#Обработчик диалога
conv_handler = ConversationHandler(
    entry_points=[CommandHandler("fun", fun)],
    states={
        TYPING_CHOICE: [
            MessageHandler(
                filters.TEXT & ~(filters.COMMAND | filters.Regex("^Готово$")), regular_choice
            )
        ],
        TYPING_REPLY: [
            MessageHandler(
                filters.TEXT & ~(filters.COMMAND | filters.Regex("^Готово$")),
                received_information,
            )
        ],
    },
    fallbacks=[MessageHandler(filters.Regex("^Готово$"), done)],
)