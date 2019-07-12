import telebot
import config
import datetime
import pytz
import json
import traceback
# from telebot import types

bot = telebot.TeleBot("856375116:AAEko6yafx2HLIGnThlZAA4F-HTMted_qww")


@bot.message_handler(commands=['start'])
def start_command(message):
    bot.send_message(message.chat.id,"Hello")

@bot.message_handler(commands=['help'])
def help_command(message):
   keyboard = telebot.types.InlineKeyboardMarkup()
   keyboard.add(
       telebot.types.InlineKeyboardButton('Message Ha Mat Lon', url='pornhub.com'
       )
   )
   bot.send_message(
       message.chat.id,
       'An nut duoi de bat ngo',
       reply_markup=keyboard
   )

@bot.message_handler(commands=['game'])
def game_command(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.row(telebot.types.InlineKeyboardButton('PUBG', callback_data='get-PUBG'))
    keyboard.row(telebot.types.InlineKeyboardButton('LOL', callback_data='get-LOL'))
    keyboard.row(telebot.types.InlineKeyboardButton('Hung Bia', callback_data='get-HB'))
    bot.send_message(message.chat.id,'choose 1 game:', reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def iq_callback(query):
    data = query.data
    if data.startswith('get-'):
       get_ex_callback(query)

def get_ex_callback(query):
    bot.answer_callback_query(query.id)
    send_exchange_result(query.message, query.data[4:])

def send_exchange_result(message, ex_code):
    # bot.send_chat_action(message.chat.id, 'typing')
    # ex = pb.get_exchange(ex_code)
    text = "day la game" + ex_code
    bot.send_message(
       message.chat.id, text
    )
  



@bot.message_handler(func=lambda message: True)
def echo_all(message):
	bot.reply_to(message, message.text)

bot.polling(none_stop=True)
