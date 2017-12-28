from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Numeric, String, Enum, ForeignKey
import enum
import somestuff

#Preparation of MYSQL Alchemy and creating tables
my_database = 'mysql+mysqldb://root:' + somestuff.mysql_pass + '@localhost/grocerylist'
engine = create_engine(my_database)

connection = engine.connect()

Base = declarative_base()
session = sessionmaker(bind=engine)

class MyEnum(enum.Enum):
    szt = "szt"
    kg = "kg"

class Category(Base):
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True)
    name = Column(String(25), nullable=False)

class Product(Base):
    __tablename__ = 'product'
    id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False)
    quantity = Column(Integer, nullable=False)
    type = Column(Enum(MyEnum), nullable=False)
    category_id = Column(Integer, ForeignKey('category.id'))
    description = Column(String(255))

    category = relationship("Category",
                            backref=backref('products'))

Base.metadata.create_all(engine)


class Item(object):
    def __init__(self, name, quantity, type, category, description):
        self.name = name
        self.quantity = quantity
        self.type = type
        self.category = category
        self.description = description



        category_msg_template = {"1": "Vegetables", "2": "Fruits", "3": "Dairy products", "4": "Meat", "5": "Chemistry",
                             "6": "Cosmetics", "7": "Bread", "8": "Drinks", "9": "Alcohol", "10": "Snacks",
                             "11": "Others"}


    @classmethod
    def long(cls):
        return cls(
            input("Name: "),
            int(input("Quantity: ")),
            input("Type: "),
            input("Category: "),
            input("Description: ")
        )

product = Item.long()



