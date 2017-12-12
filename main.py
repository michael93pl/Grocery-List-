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
            return add_product()
        elif choice == "check" or choice == "c":
            print("funkcja_do_wyswietlania")
            break
        else:
            print("You messed up. Please choose to add a new item or check the current list only.")

def add_product():
    """Adds products according to users input"""
    name = input("Please provide the name your product\n")#name of the product
    while True:#checks if quantity is an int
        quantity = input("Please provide quantity of your product\n")
        try:
            quantity = int(quantity)
            break
        except ValueError:
            print("That's not an integer!")
            continue
    while True:#converts input of the product type into specific enum in DB
        type =input("Do you want to add pieces or kgs?\n")
        if type == "pieces" or type == "piece" or type == "kg" or type == "kgs":
            break
        else:
            print("Hey mate, please use only 'piece' or 'kg'")
    if type == "pieces" or type == "piece":
        type = "pieces"
    else:
        type = "kgs"

    for k, v in category_msg_template.items(): #prints dictionary to display categories
        print(k, v)
    while True: #prints key of the category dict for both key and value input
        category = input("\nPick one of the above categories:\n").title()
        if category in category_msg_template:
            break
        elif category in category_msg_template.values():
            for key, value in category_msg_template.items():
                if category == value:
                    category = key
            break
        else:
            print("Are You sure you chose correct category?")

    decision_for_description = input("Do you want to add any description?\n").lower()
    if decision_for_description == "yes" or decision_for_description == "y":
        while True:
            description = input("Please provide valid description of your product\n")
            if len(description) > 255:
                print("Hey, maximum description length is 255 characters!")
            else:
                break
    else:
        description = ""
    global product
    product = (name, quantity, type, category, description)

    return display_ready_product()

def display_ready_product():
    print(product)

if __name__ == "__main__":
    first_choise()