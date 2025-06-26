import threading
from DataBase.DBManager import DBManager
from Setup import bot
from TGBot import CommandHandlers
from TGBot import MessageHandlers

if __name__ == "__main__":
    db_manager = DBManager()
    threading.Thread(target=db_manager.scheduler,daemon=True).start()
    db_manager.scheduler()
    bot.infinity_polling()