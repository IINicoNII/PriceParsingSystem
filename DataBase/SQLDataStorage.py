from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, create_engine, Boolean,ARRAY
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.dialects.postgresql import ARRAY as PG_ARRAY
from datetime import datetime

Base = declarative_base()


class Product(Base):
    __tablename__ = "products"
    ID = Column(Integer, primary_key=True, autoincrement=True)
    ProductName = Column(String)
    ProductID = Column(Integer)
    IsTracked = Column(Boolean)
    LastTracked = Column(DateTime)
    PriceBase = Column(PG_ARRAY(Integer))
    PriceDiscount = Column(PG_ARRAY(Integer))
    PriceCard = Column(PG_ARRAY(Integer))

# нужно создать пользователя в postgres и задать ему пароль
# заменить в строке ниже "crunchy:123" на "[имя пользователя]:[пароль]"
DATABASE_URL = "postgresql://postgres:14Lb!Dj08@localhost:5432/price_tracking"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


if __name__ == "__main__":
    print("База данных и таблицы созданы!")