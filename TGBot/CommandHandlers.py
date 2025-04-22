from Setup import bot
from telebot import types
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('Добавить новый артикул')
    bot.reply_to(message, "Привет! Я бот.", reply_markup=markup)