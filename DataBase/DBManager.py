from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from DataBase.SQLDataStorage import DATABASE_URL,Product
from Parsing.OZON import OzonParser


class DBManager:
    def __init__(self):
        self.engine = create_engine(DATABASE_URL)
        self.Session = sessionmaker(bind=self.engine)


    def add_product(self,productID):
        session = self.Session()
        inspector = OzonParser()
        product_info = inspector.get_info_by_id(productID)

        new_product = Product(
            ProductName = product_info['Название'],
            ProductID=productID,
            IsTracked=True,
            PriceBase=[product_info['Базовая цена']],
            PriceDiscount=[product_info['Цена со скидкой']],
            PriceCard=[product_info['Цена по карте']],
            LastTracked=datetime.now()
        )
        session.add(new_product)
        session.commit()
        session.close()


    def update_product(self,productID):
        session = self.Session()
        inspector = OzonParser()
        product_info = inspector.get_info_by_id(productID)
        product = session.query(Product).filter_by(ProductID=productID).first()
        product.ProductName = product_info['Название']
        product.PriceBase = product.PriceBase + [product_info['Базовая цена']]
        product.PriceCard = product.PriceCard + [product_info['Цена по карте']]
        product.PriceDiscount = product.PriceDiscount + [product_info['Цена со скидкой']]
        session.commit()
        session.close()



