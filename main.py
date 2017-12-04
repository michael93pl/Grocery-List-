from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Numeric, String, Enum, ForeignKey
import enum
import somestuff

my_database = 'mysql+mysqldb://root:' + somestuff.mysql_pass + '@localhost/grocerylist'
engine = create_engine(my_database, echo=True)

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





print("Hello dear User!\nYou can either add new items to your grocery list or check your list\nWhat would you like to do? Please choose add or check only.")

def template():
    msg_template = """
    
                """
    pass


def first_choise():
    """checking input"""
    while True:
        choice = input().strip().lower()
        if choice == "add" or choice == "a":
            print(funkcja_do_dodawania(10,15))
            break
        elif choice == "check" or choice == "c":
            print(funkcja_do_wyswietlania(300,500))
            break
        else:
            print("You messed up. Please choose add new item or check the current list only.")


def funkcja_do_dodawania(kupa, siku):
    kibelek = kupa + siku

    return kibelek


def funkcja_do_wyswietlania(cipka, kutas):
    lista = cipka + kutas

    return lista








if __name__ == "__main__":
    first_choise()



#Grocery list app with MySQL

"""czy chcesz dodac // czy chcesz wczytac

wyswietlac cala baze, same kategorie (oby dwie z description)



!!!znaleźć operacje na metodach, zeby przetestować klasy !!!


dodawania / odejmowanie / usuwanie itemow


"""