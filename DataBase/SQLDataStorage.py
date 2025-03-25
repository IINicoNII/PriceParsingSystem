from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from datetime import datetime

Base = declarative_base()


class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    url = Column(String, unique=True)
    current_price = Column(Float)
    lowest_price = Column(Float)
    last_updated = Column(DateTime, default=datetime.now)


class PriceHistory(Base):
    __tablename__ = "price_history"
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    price = Column(Float)
    date = Column(DateTime, default=datetime.now)

engine = create_engine('PostgreSQL:///prices.db') # прописать по другому( в данном случае это для SQLite)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()