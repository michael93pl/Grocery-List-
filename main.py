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


print("Hello dear User!\nYou can either add new items to your grocery list or check your list\nWhat would you like to do? Please choose 'add' or 'check' only.")


#category template with the category printing function
category_msg_template = ["1. Vegetables/Fruits", "2. Dairy products", "3. Meat", "4. Chemistry",
                        "5. Cosmetics", "6. Bread", "7. Drinks", "8. Alkohol", "9. Snacks", "10. Others"]


def category_printing():
    for i in category_msg_template:
        print(i)

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
    """Inserting data into database"""
    print("At first pick one of the following categories:\n")
    return category_printing()

    while True:
        category_choise = input().strip().lower()
        if category_choise == "1" or category_choise == "vegetables":
            print("Twoja stara")

def funkcja_do_wyswietlania(cipka, kutas):
    lista = cipka + kutas

    return lista

if __name__ == "__main__":
    first_choise()
