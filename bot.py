import telebot, os
from config import *
from logic import *
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

bot = telebot.TeleBot(token)



cancel_button = "Отмена 🚫"
def gen_markup(rows):
    markup = ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.row_width = 1
    for row in rows:
        markup.add(KeyboardButton(row))
    markup.add(KeyboardButton(cancel_button))
    return markup



@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, '''Добро пожаловать в бот тех-поддержки интернет-магазина "Продаем все на свете".
    Воспользуйтесь командой /question для вывода всех базовых вопросов
    ''')

@bot.message_handler(commands=['question'])
def send_welcome(message):
    bot.send_message(message.chat.id, '''/q1 - Как оформить заказ?
    /q2 - Как узнать статус моего заказа?
    /q3 - Как отменить заказ?
    /q4 - Что делать, если товар пришел поврежденным?
    /q5 - Как связаться с вашей технической поддержкой?
    /q6 - Как узнать информацию о доставке?
    /special — если вы не нашли нужный вопрос, мы можем перенаправить вас к специалисту
    ''')


@bot.message_handler(commands=['q1'])
def send_welcome(message):
    bot.send_message(message.chat.id, '''Для оформления заказа, пожалуйста, выберите интересующий вас товар и нажмите кнопку "Добавить в корзину", затем перейдите в корзину и следуйте инструкциям для завершения покупки.
''')

@bot.message_handler(commands=['q2'])
def send_welcome(message):
    bot.send_message(message.chat.id, ''' Вы можете узнать статус вашего заказа, войдя в свой аккаунт на нашем сайте и перейдя в раздел "Мои заказы". Там будет указан текущий статус вашего заказа.
''')

@bot.message_handler(commands=['q3'])
def send_welcome(message):
    bot.send_message(message.chat.id, ''' Если вы хотите отменить заказ, пожалуйста, свяжитесь с нашей службой поддержки как можно скорее. Мы постараемся помочь вам с отменой заказа до его отправки.
''')

@bot.message_handler(commands=['q4'])
def send_welcome(message):
    bot.send_message(message.chat.id, ''' При получении поврежденного товара, пожалуйста, сразу свяжитесь с нашей службой поддержки и предоставьте фотографии повреждений. Мы поможем вам с обменом или возвратом товара.
''')

@bot.message_handler(commands=['q5'])
def send_welcome(message):
    bot.send_message(message.chat.id, ''' Вы можете связаться с нашей технической поддержкой через телефон на нашем сайте или написать нам в чат-бота.
''')

@bot.message_handler(commands=['q6'])
def send_welcome(message):
    bot.send_message(message.chat.id, ''' Информацию о доставке вы можете найти на странице оформления заказа на нашем сайте. Там указаны доступные способы доставки и сроки.
''')


@bot.message_handler(commands=['special'])
def get_question(message):
    bot.send_message(message.chat.id, "Введите вопрос:")
    bot.register_next_step_handler(message, name_q)


def name_q(message):
    question = message.text
    data=[question]
    specialists = [x[0] for x in manager.get_specialist()] #тоже самое в лоджик
    bot.send_message(message.chat.id, "Введите специалиста", reply_markup=gen_markup(specialists))
    bot.register_next_step_handler(message, callback_quest, data=data, specialists=specialists)


def callback_quest(message, data, statuses):
    specialist = message.text
    if message.text == cancel_button:
        specialist(message)
        return
    if specialist not in specialists:
        bot.send_message(message.chat.id, "Ты выбрал специалиста не из списка, попробуй еще раз!)",
        reply_markup=gen_markup(statuses))
        bot.register_next_step_handler(message, callback_quest, data=data, specialists=specialists)
        return
    specialist = manager.get_specialist_id(specialist) #доработать get_specialist_id в лоджик
    data.append(specialist)
    manager.insert_quest([tuple(data)])
    bot.send_message(message.chat.id, "Вопрос сохранен")


if __name__ == '__main__':
    manager = DatabaseManager(database)
    bot.infinity_polling()
