import telebot
import config
import datetime
import pytz
import json
import traceback
import db


bot = telebot.TeleBot("899548678:AAHsHPkBAbrLb2OrCjYNC5mGh809CF1HSvM")


products = db.get_all_products()
questions = db.get_all_questions()

@bot.message_handler(commands=['start'])
def start_command(message):
    text = """
    hello i'm Ruby ml!
hit /product to see the list
    """
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['product'])
def product_command(message):
    keyboard = telebot.types.InlineKeyboardMarkup()

    for product in products:
        keyboard.row(telebot.types.InlineKeyboardButton('{}'.format(product['product']), callback_data='{}'.format(product['product'])))

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
    if data.startswith('fb-'):
        get_feedback_callback(query)
    if data == 'back2':
        product_command(query.message)
    
    
def get_ex_callback(query):
    bot.answer_callback_query(query.id)
    send_result(query.message, query.data[1:10],query.data[11:])

def get_feedback_callback(query):
    bot.answer_callback_query(query.id)
    send_result_feedback(query.message, query.data[4:])


def send_result(message, ex_code1, ex_code2):
    a = db.get_question_by_product_and_question(ex_code1,ex_code2)
    text = a['answer']
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.row(telebot.types.InlineKeyboardButton('Back', callback_data='back2'))
    bot.send_message(message.chat.id,text,reply_markup=keyboard)

def send_result_feedback(message, ex_code):
    db.insert_feedback(ex_code,)
    bot.send_message(message.chat.id,text,reply_markup=keyboard)


@bot.message_handler(regexp='uby')
def handle_message(message):
	bot.send_message(
        message.chat.id, "Chat with me @duypzo_bot"
    )



bot.polling(none_stop=True)