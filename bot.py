import telebot
import config
import datetime
import pytz
import json
import traceback
import db
# from telebot import types

bot = telebot.TeleBot("856375116:AAEko6yafx2HLIGnThlZAA4F-HTMted_qww")


# @bot.message_handler(commands=['start'])
# def start_command(message):
#     bot.send_message(message.chat.id,"Hello")

# @bot.message_handler(commands=['help'])
# def help_command(message):
#    keyboard = telebot.types.InlineKeyboardMarkup()
#    keyboard.add(
#        telebot.types.InlineKeyboardButton('Message Ha Mat Lon', url='pornhub.com'
#        )
#    )
#    bot.send_message(
#        message.chat.id,
#        'An nut duoi de bat ngo',
#        reply_markup=keyboard
#    )
options = db.get_all_options()

@bot.message_handler(commands=['start'])
def start_command(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    for i in range(0,len(options),2):
        keyboard.row(telebot.types.InlineKeyboardButton(options[i]['option'], callback_data='get-{}'.format(options[i]['option'])),
                    telebot.types.InlineKeyboardButton(options[i+1]['option'], callback_data='get-{}'.format(options[i+1]['option'])))
    
    keyboard.row(telebot.types.InlineKeyboardButton('Back', callback_data='back'))

    bot.send_message(message.chat.id,'choose 1 button:', reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def iq_callback(query):
    data = query.data
    if data.startswith('get-'):
        get_ex_callback(query)
    if data == 'back':
        start_command(query.message)


def get_ex_callback(query):
    bot.answer_callback_query(query.id)
    send_result(query.message, query.data[4:])

def send_result(message, ex_code):
    a = db.get_option(ex_code)
    text = a['reply']
    bot.send_message(
       message.chat.id, text
    )

def get_ex_callback1(query):
    bot.answer_callback_query(query.id)
    send_result1(query.message)

def send_result1(message):
    text = "This is back button "
    bot.send_message(
       message.chat.id, text
    )




@bot.message_handler(func=lambda message: True)
def echo_all(message):
	bot.reply_to(message, message.text)

bot.polling(none_stop=True)
