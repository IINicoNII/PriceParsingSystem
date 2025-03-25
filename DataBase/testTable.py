from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class TestModel(Base):
    __tablename__ = "test_table"
    id = Column(Integer, primary_key=True)
    name = Column(String)

engine = create_engine("sqlite:///test.db")
Base.metadata.create_all(engine)

print("Таблица создана! SQLAlchemy работает.")