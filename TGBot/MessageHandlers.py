from Setup import *
from telebot import types


def update_state(chat_id, new_state):
    db_manager.update_state_db(chat_id, new_state)
    user_states[chat_id] = new_state

def gen_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('Добавить новый артикул')
    markup.add('Удалить артикул')

    return markup
@bot.message_handler(func=lambda message: 'Добавить новый артикул' in message.text)
def add_product_id(message):
    update_state(message.chat.id, 'add')
    bot.send_message(message.chat.id, 'Введите артикул или ссылку на товар, который вы хотите добавить')

@bot.message_handler(func=lambda message: 'Удалить артикул' in message.text)
def remove_product_id(message):
    update_state(message.chat.id, 'remove')
    bot.send_message(message.chat.id, 'Введите артикул товара, который вы хотите удалить')

@bot.message_handler(func=lambda message: message.text.isdigit())
def change_product_id(message):
    product_ID = int(message.text)
    if user_states[message.chat.id] == 'add':
        if not db_manager.user_traking_product(product_ID, message.chat.id):
            if db_manager.check_exists(product_ID):
                db_manager.start_tracking(product_ID)
            else:
                db_manager.add_product(product_ID)
                db_manager.start_tracking(product_ID)
            db_manager.link_product_to_user(product_ID, message.chat.id)
            bot.send_message(message.chat.id, f'Товар с артикулом {product_ID} добавлен для отслеживания',
                             reply_markup=gen_markup())
        else:
            bot.send_message(message.chat.id, f'Товар с артикулом {product_ID} уже отслеживается',
                             reply_markup=gen_markup())


    if user_states[message.chat.id] == 'remove':
        if not db_manager.check_exists(product_ID):
            bot.send_message(message.chat.id, f'Товар с артикулом {product_ID} не найден в базе', reply_markup=gen_markup())
        elif not db_manager.user_traking_product(product_ID, message.chat.id):
            bot.send_message(message.chat.id, f'Товар с артикулом {product_ID} в настоящий момент не отслеживается', reply_markup=gen_markup())
        else:
            db_manager.remove_product_from_user(product_ID, message.chat.id)
            users = db_manager.get_all_users()
            is_tracked = False
            for chatID in users:
                if db_manager.user_traking_product(product_ID, chatID):
                    is_tracked = True
            if not is_tracked:
                db_manager.stop_tracking(product_ID)
            bot.send_message(message.chat.id, f'Товар с артикулом {product_ID} больше не отслеживается')
    update_state(message.chat.id, 'default')


@bot.message_handler(func=lambda message: True)
def send_welcome(message):
    bot.reply_to(message, message.text, reply_markup=gen_markup())
