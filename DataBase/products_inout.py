from DataBase.SQLDataStorage import SessionLocal, Product
from sqlalchemy import text
from typing import List

# 1. Создаём сессию
db = SessionLocal()


# 2. Добавляем новый товар
def add_product(productName: str,
                productID: int,
                isTracked: bool,
                priceBase: List[int] = [],
                priceDiscount: List[int] = [],
                priceCard: List[int] = [],
                lastTracked: str = None):
    new_product = Product(
        ProductName=productName,
        ProductID=productID,
        IsTracked=isTracked,
        PriceBase=priceBase,
        PriceDiscount=priceDiscount,
        PriceCard=priceCard,
        LastTracked=lastTracked
    )
    db.add(new_product)
    db.commit()

    print(f"Добавлен: {productName}")


# 4. Получаем все товары
def get_products():
    products = db.query(Product).all()
    for product in products:
        print(f"{product.ProductID}: {product.ProductName}")


def truncate_products():
    db.execute(text("TRUNCATE TABLE products RESTART IDENTITY CASCADE"))
    db.commit()
    print("Таблица products полностью очищена (сброс ID)")