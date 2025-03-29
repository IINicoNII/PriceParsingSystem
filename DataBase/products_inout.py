from DataBase.SQLDataStorage import SessionLocal, Product, PriceHistory
from sqlalchemy import text

# 1. Создаём сессию
db = SessionLocal()


# 2. Добавляем новый товар
def add_product(name: str, url: str, price: float):
    new_product = Product(
        name=name,
        url=url,
        current_price=price,
        lowest_price=price,
    )
    db.add(new_product)
    db.commit()

    # Добавляем запись в историю цен
    history = PriceHistory(
        product_id=new_product.id,
        price=price,
    )
    db.add(history)
    db.commit()
    print(f"Добавлен: {name}")


# 3. Обновляем цену товара
def update_price(product_id: int, new_price: float):
    product = db.get(Product, product_id)
    if not product:
        print("Товар не найден!")
        return

    product.current_price = new_price
    if new_price < product.lowest_price:
        product.lowest_price = new_price

    # Фиксируем изменение в истории
    history = PriceHistory(
        product_id=product.id,
        price=new_price,
    )
    db.add(history)
    db.commit()
    print(f"Обновлена цена: {product.name} → {new_price}")


# 4. Получаем все товары
def get_products():
    products = db.query(Product).all()
    for product in products:
        print(f"{product.id}: {product.name} ({product.current_price} руб.)")

def truncate_products():
    db.execute(text("TRUNCATE TABLE products RESTART IDENTITY CASCADE"))
    db.commit()
    print("Таблица products полностью очищена (сброс ID)")