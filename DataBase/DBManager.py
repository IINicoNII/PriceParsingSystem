from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from DataBase.SQLDataStorage import DATABASE_URL,Product
from Parsing.OZON import OzonParser
from typing import List
import schedule
import time


class DBManager:
    def __init__(self):
        self.engine = create_engine(DATABASE_URL)
        self.Session = sessionmaker(bind=self.engine)

    def add_product(self, productID, isTracked=True):
        try:
            with self.Session() as session, session.begin():
                # Проверка существования артикула
                if session.query(Product).filter_by(ProductID=productID).first():
                    print(f'Товар с артикулом {productID} уже есть в БД!')
                    return False

                inspector = OzonParser()
                product_info = inspector.get_info_by_id(productID)

                new_product = Product(
                    ProductName=product_info['Название'],
                    ProductID=productID,
                    IsTracked=isTracked,
                    PriceBase=[product_info['Базовая цена']],
                    PriceDiscount=[product_info['Цена со скидкой']],
                    PriceCard=[product_info['Цена по карте']],
                    TrackingTime=[datetime.now()]
                )
                session.add(new_product)
                print(f'Артикул {productID} добавлен в БД!')
                return True

        except Exception as e:
            print(f'Ошибка при добавлении товара {productID}: {str(e)}')
            return False

    def update_product(self, productID):
        session = self.Session()
        inspector = OzonParser()
        product_info = inspector.get_info_by_id(productID)
        product = session.query(Product).filter_by(ProductID=productID).first()
        if product.IsTracked:
            product.ProductName = product_info['Название']
            product.PriceBase = product.PriceBase + [product_info['Базовая цена']]
            product.PriceCard = product.PriceCard + [product_info['Цена по карте']]
            product.PriceDiscount = product.PriceDiscount + [product_info['Цена со скидкой']]
            product.TrackingTime =  product.TrackingTime + [datetime.now()]
            session.commit()
            print('Информация о товаре с артикулом {} обновлена!'.format(productID))
        else:
            print('Товар с артикулом {} не отслеживается!'.format(productID))
        session.close()

    def get_tracked_articles(self) -> List[str]:
        session = self.Session()
        stmt = select(Product.ProductID).where(Product.IsTracked)
        result = session.execute(stmt)
        session.close()
        return [row[0] for row in result]

    def update_all(self):
        all_ID = self.get_tracked_articles()
        for article in all_ID:
            self.update_product(article)

    def scheduler(self):
        schedule.every().day.at('11:56').do(self.update_all)
        schedule.every().day.at('18:00').do(self.update_all)
        while True:
            schedule.run_pending()
            time.sleep(10)