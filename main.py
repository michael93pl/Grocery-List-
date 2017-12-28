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

print("Hello dear User!\nYou can either add new items to your grocery list or check your list.\n\n")

#category template with the category printing function
category_msg_template = {"1": "Vegetables", "2": "Fruits", "3": "Dairy products", "4": "Meat", "5": "Chemistry",
            "6": "Cosmetics", "7": "Bread", "8": "Drinks", "9": "Alcohol", "10": "Snacks", "11": "Others"}

def first_choise():
    """checking if the user wants to add the new item or view the whole list"""
    while True:
        choice = input("What would you like to do? Please choose 'Add' or 'Check' only.").lower()
        if choice in ("add", "a"):
            return gather()
        elif choice in ("check", "c"):
            print("funkcja_do_wyswietlania")
            break
        else:
            print("You messed up. Please choose to add a new item or check the current list only.")

def get_name():
    """gets name input"""
    name = input("Please provide the name your product.\n")#name of the product
    return name

def get_quantity():
    """gets quantity input"""
    while True:#checks if quantity is an int
        quantity = input("Please provide quantity of your product.\n")
        try:
            quantity = int(quantity)
            return quantity
        except ValueError:
            print("That's not an integer!")
            continue

def get_type():
    """gets type input"""
    while True:#converts input of the product type into specific enum in DB
        type =input("Do you want to add pieces or kgs?\n")
        if type in ("pieces", "piece",  "kg", "kgs"):
            break
        else:
            print("Hey mate, please use only 'piece' or 'kg'.")
    if type in ("pieces", "piece"):
        type = "pieces"
    else:
        type = "kgs"

    return type

def get_category():
    """gets category input"""
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
    return category

def get_decision(question):
    """decision for description"""
    decision = False
    while True:
        decision_for_description = input(question).lower()
        if decision_for_description in ("y", "yes"):
            decision = True
            break
        if decision_for_description in ('n', 'no'):
            break
        print("Please choose yes or no.")
    return decision

def get_description():
    """gets description input"""
    while True:
        description = input("Please provide valid description of your product.\n")
        if len(description) > 255:
            print("Hey, maximum description length is 255 characters!")
        else:
            break
    return description

def gather():
    """gathers all inputs into one function"""
    name = None
    name = get_name()
    quantity = None
    quantity = get_quantity()
    type = None
    type = get_type()
    category = None
    category = get_category()
    description = " "

    add_description = get_decision("Do you want to add any description?\n")
    if add_description:
        description = get_description()

    for k, v in category_msg_template.items():  # converts category into value of a dict just to display for the user
        if category == k:
            category = v
    display_product = "Name : {}\nQuantity: {}\nType: {}\nCategory: {}\nDescription: {}".format(name, quantity, type, category, description)
    print(display_product)

    while True: #asks if user wants to change any aspect of the product
        changes = input("\nDo You want to change any aspect of your product?\n").lower()
        if changes in ("yes", "y"):
            break
        if changes in ("no", "n"):
            return function_after_no_in_aspect_changing()
        else:
            print("Please, choose yes or no!")

    final_product = (name, quantity, type, category, description)

    for k, v in category_msg_template.items():  # converts category into key of a dict to use with instances
        if category == v:
            category = k

    class Item(object):

        def __init__(self, name, quantity, type, category, description):
            self.name = name
            self.quantity = quantity
            self.type = type
            self.category = category
            self.description = description

        def printing_product(self):
            return "{} {} {} {} {}".format(self.name, self.quantity, self.type, self. category, self.description)

        def change_name(self,):
            self.name = new_name
            return new_name

        def change_quantity(self):
            pass

        def change_type(self):
            pass

        def change_category(self):
            pass

        def change_description(self):
            pass

    product = Item(name, quantity, type, category, description)
    print(display_product)

    while True:
        choise = input("Which attribute do you want to change?\n").lower()
        if choise in ("name", "1", "n"):
            print("run first method")
            new_name = input("Provide new name of your product")
            product.change_name()
            print(product.change_name())
            break
        if choise in ("quantity", "2", "q"):
            print("run 2nd method")
            break
        if choise in ("type", "3", "t"):
            print("run 3rd method")
            break
        if choise in ("category", "4", "c"):
            print("run 4t method")
            break
        if choise in ("description", "5", "d"):
            print("run 5th method")
            break
        else:
            print("You messed up, pick the correct attribute you want to change")


def function_after_no_in_aspect_changing():  # function displaying possibilities after product confirmation
    pass


if __name__ == "__main__":
    first_choise()
