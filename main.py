from DataBase.DBManager import DBManager

if __name__ == "__main__":
    db_manager = DBManager()
    db_manager.add_product(1827580929, isTracked=False)
    db_manager.add_product(1937862493)
    db_manager.update_all()