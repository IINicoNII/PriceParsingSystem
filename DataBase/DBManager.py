from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from DataBase.SQLDataStorage import DATABASE_URL, Product,User
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

    def start_tracking(self, productID):
        session = self.Session()
        product = session.query(Product).filter_by(ProductID=productID).first()
        product.IsTracked = True
        session.commit()
        session.close()

    def stop_tracking(self, productID):
        session = self.Session()
        product = session.query(Product).filter_by(ProductID=productID).first()
        product.IsTracked = False
        session.commit()
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

    def check_exists(self, productID):
        session = self.Session()
        result = session.query(Product).filter_by(ProductID=productID).first()
        session.close()
        return bool(result)

    def register_user(self,chatID):
        session = self.Session()
        new_user = User(
            ChatID = chatID,
            TrackedProducts=[]
        )
        session.add(new_user)
        session.commit()
        session.close( )
        print(f'Пользователь {chatID} добавлен в БД!')

    def check_exists_user(self, chatID):
        session = self.Session()
        result = session.query(User).filter_by(ChatID=chatID).first()
        session.close()
        return bool(result)

    def link_product_to_user(self, productID, chatID):
        self.add_product(productID)
        if not self.check_exists_user(chatID):
            self.register_user(chatID)
        session = self.Session()
        user = session.query(User).filter_by(ChatID=chatID).first()
        user.TrackedProducts = user.TrackedProducts + [productID]
        session.commit()
        session.close()

    def remove_product_from_user(self, productID, chatID):
        session =self.Session()
        user = session.query(User).filter_by(ChatID=chatID).first()
        products = user.TrackedProducts.copy()
        products.remove(productID)
        session.commit()
        session.close()

    def user_traking_product(self, chatID, productID):
        """
        Метод для получения информации отслеживает ли пользователь артикул или нет
        :param chatID:
        :param productID:
        :return:
        """
        session = self.Session()
        user = session.query(User).filter_by(ChatID=chatID).first()
        session.close()
        if productID in user.TrackedProducts:
             return True
        return False


    def get_all_users(self):
        session = self.Session()
        user_list = session.query(User.chat_id).all()
        session.close()
        return [row[0] for row in user_list]


