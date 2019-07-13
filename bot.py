import telebot
import config
import datetime
import pytz
import json
import traceback
import db


bot = telebot.TeleBot("856375116:AAEko6yafx2HLIGnThlZAA4F-HTMted_qww")


products = db.get_all_products()
questions = db.get_all_questions()

@bot.message_handler(commands=['welcome'])
def welcome(message):
    text = """
Hello, this is Ha pho lon Q&A's bot
/start to begin
    """
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['start'])
def start_command(message):
    keyboard = telebot.types.InlineKeyboardMarkup()

    for product in products:
        keyboard.row(telebot.types.InlineKeyboardButton('{}'.format(product['product']), callback_data='{}'.format(product['product'])))
    keyboard.row(telebot.types.InlineKeyboardButton(
        'Back', callback_data='back1'))

    bot.send_message(message.chat.id, 'choose 1 product:',
                     reply_markup=keyboard)


@bot.message_handler(commands=['question'])
def question_command(message,questions):
    keyboard = telebot.types.InlineKeyboardMarkup()
    for question in questions:
        keyboard.row(telebot.types.InlineKeyboardButton('{}'.format(question['question']), callback_data='-{}-{}'.format(question['product'],question['question'])))
    keyboard.row(telebot.types.InlineKeyboardButton(
        'Back', callback_data='back2'))
    bot.send_message(message.chat.id, 'choose 1 question:',
                     reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def iq_callback(query):
    data = query.data
    for product in products:
        if data == product['product']:
            question_command(query.message,db.get_question_by_product(product['product']))
    if data.startswith('-'):
        get_ex_callback(query)
    if data == 'back1':
        welcome(query.message)
    if data == 'back2':
        start_command(query.message)
    
    
def get_ex_callback(query):
    bot.answer_callback_query(query.id)
    send_result(query.message, query.data[1:10],query.data[11:])


def send_result(message, ex_code1, ex_code2):
    a = db.get_question_by_product_and_question(ex_code1,ex_code2)
    text = a['answer']
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.row(telebot.types.InlineKeyboardButton('Back', callback_data='back2'))
    bot.send_message(message.chat.id,text,reply_markup=keyboard)


@bot.message_handler(regexp='{}'.format(i for i in ['cac','chim']))
def handle_message(message):
	bot.send_message(
        message.chat.id, "Ha mat lon"
    )


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)


bot.polling(none_stop=True)
