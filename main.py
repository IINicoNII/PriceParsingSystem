from DataBase.DBManager import DBManager

if __name__ == "__main__":
    db_manager = DBManager()
    #db_manager.update_product(1937862493)
    #db_manager.update_product(1821495135)
    db_manager.get_tracked_articles()