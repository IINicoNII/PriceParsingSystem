from DataBase.products_inout import *

if __name__ == "__main__":
    add_product("iPhone 15", "https://amazon.com/iphone15", 999.99)
    add_product("Samsung S23", "https://amazon.com/s23", 799.99)

    update_price(1, 899.99)  # Обновляем цену iPhone

    get_products()  # Вывод всех товаров
    truncate_products()
    db.close()  # Закрываем сессию