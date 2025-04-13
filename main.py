from DataBase.products_inout import *

if __name__ == "__main__":
    add_product("iPhone 15", 255, isTracked=True)
    add_product("Samsung S23", 471, isTracked=False)

    get_products()  # Вывод всех товаров
    #truncate_products()
    db.close()  # Закрываем сессию