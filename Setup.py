import telebot
from config import token
from DataBase.DBManager import DBManager


bot = telebot.TeleBot(token)
db_manager = DBManager()
user_states = db_manager.fetch_all_states()