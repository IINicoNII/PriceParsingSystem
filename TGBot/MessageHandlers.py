from Setup import *
from telebot import types

def gen_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('Добавить новый артикул')
    markup.add('Удалить артикул')

    return markup
@bot.message_handler(func=lambda message: 'Добавить новый артикул' in message.text)
def add_product_id(message):
    user_states[0] = 'add'
    bot.send_message(message.chat.id, 'Введите артикул или ссылку на товар, который вы хотите добавить')

@bot.message_handler(func=lambda message: 'Удалить артикул' in message.text)
def add_product_id(message):
    user_states[0] = 'remove'
    bot.send_message(message.chat.id, 'Введите артикул товара, который вы хотите удалить')

@bot.message_handler(func=lambda message: message.text.isdigit())
def change_product_id(message):
    product_ID = int(message.text)
    if user_states[0] == 'add':
        if db_manager.check_exists(product_ID):
            db_manager.start_tracking(product_ID)
        else:
            db_manager.add_product(product_ID)
    db_manager.link_product_to_user(product_ID, message.chat.id)
    bot.send_message(message.chat.id, f'Товар с артикулом {product_ID} добавлен для отслеживания',
                     reply_markup=gen_markup())

    if user_states[0] == 'remove':
        if db_manager.add_product(product_ID):
            db_manager.update_product(product_ID, False)
            bot.send_message(message.chat.id, f'Товар {product_ID} больше не отслеживается')
        # мы перестаем отслеживать товар
        else:
            bot.send_message(message.chat.id, f'Товар {product_ID} не найден в базе')



@bot.message_handler(func=lambda message: True)
def send_welcome(message):
    bot.reply_to(message, message.text, reply_markup=gen_markup())
