import telebot
from config import token
from DataBase.DBManager import DBManager

user_states = {0: 'add'}
bot = telebot.TeleBot(token)
db_manager = DBManager()