from DataBase.SQLDataStorage import Product, session


def add_product(name: str, url: str, price: float):
    existing_product = session.query(Product).filter_by(url=url). first()
    if existing_product:
        print("Товар уже отслеживается!")
        return existing_product

    new_