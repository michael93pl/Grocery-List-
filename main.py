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

print("Hello dear User!\nYou can either add new items to your grocery list or check your list.\n\nWhat would you like to do? Please choose 'Add' or 'Check' only.")

#category template with the category printing function
category_msg_template = {"1": "Vegetables", "2": "Fruits", "3": "Dairy products", "4": "Meat", "5": "Chemistry",
            "6": "Cosmetics", "7": "Bread", "8": "Drinks", "9": "Alcohol", "10": "Snacks", "11": "Others"}

def first_choise():
    """checking if the user wants to add the new item or view the whole list"""
    while True:
        choice = input().strip().lower()
        if choice == "add" or choice == "a":
            return display()
        elif choice == "check" or choice == "c":
            print(funkcja_do_wyswietlania(300,500))
            break
        else:
            print("You messed up. Please choose to add a new item or check the current list only.")

def display():
    """Displaying categories and to choose the correct one"""
    for k, v in category_msg_template.items():
        print(k, v)
    while True:
        category = input("\nAt first pick one of the above categories:\n").title()
        if category in category_msg_template or category in category_msg_template.values():
            if category == "1" or category == "Vegetables":
                print("Warzywka")
            elif category == "2" or category == "Fruits":
                print("Owocki")
            elif category == "3" or category == "Dairy products":
                print("nabial")
            elif category == "4" or category == "Meat":
                print("Miesko")
            elif category == "5" or category == "Chemistry":
                print("chemia")
            elif category == "6" or category == "Cosmetics":
                print("kosmetyki")
            elif category == "7" or category == "Bread":
                print("pieczywko")
            elif category == "8" or category == "Drinks":
                print("napoje")
            elif category == "9" or category == "Alcohol":
                print("alko")
            elif category == "10" or category == "Snacks":
                print("przekaski")
            elif category == "11" or category == "Others":
                print("inne")
        else:
            print("Are You sure you chose correct category?")


def funkcja_do_wyswietlania(x, y):
    lista = x + y

    return lista

if __name__ == "__main__":
    first_choise()
