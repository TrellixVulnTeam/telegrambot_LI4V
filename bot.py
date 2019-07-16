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

@bot.message_handler(commands=['start'])
def start_command(message):
    text = """
    hello i'm Ruby ml!
hit /help to see the list
hit /feedback to send your question
    """
    bot.send_message(message.chat.id, text)



@bot.message_handler(commands=['help'])
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


@bot.message_handler(commands=['feedback'])
def feedback_command(message):
    text = """
    Type in form to send your question
[ditmeha]_[Product]_[Your question]
	"""
    bot.send_message(message.chat.id, text)


@bot.message_handler(regexp='ditmeha_')
def fb_process(message):
    message_split = message.text.split('_')
    product = message_split[1]
    content = message_split[2]
    db.insert_feedback(product,content)
    bot.send_message(message.chat.id, "Done")


@bot.callback_query_handler(func=lambda call: True)
def iq_callback(query):
    data = query.data
    for product in products:
        if data == product['product']:
            question_command(query.message,db.get_question_by_product(product['product']))
    if data.startswith('-'):
        get_ex_callback(query)
    if data == 'back2':
        product_command(query.message)
    
    
def get_ex_callback(query):
    bot.answer_callback_query(query.id)
    data = query.data
    data_process = data.split('-')
    send_result(query.message, data_process[1],data_process[2])



def send_result(message, ex_code1, ex_code2):
    a = db.get_question_by_product_and_question(ex_code1,ex_code2)
    text = a['answer']
    print(a)
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.row(telebot.types.InlineKeyboardButton('Back', callback_data='back2'))
    bot.send_message(message.chat.id,text,reply_markup=keyboard)




@bot.message_handler(regexp='uby')
def handle_message(message):
	bot.send_message(
        message.chat.id, "Chat with me @duypzo_bot"
    )



bot.polling(none_stop=True)