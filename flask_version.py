from flask import Flask
from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, validators, SubmitField, ValidationError
from flask import render_template, redirect, url_for, request
from wtforms.validators import InputRequired, Length
from flask_sqlalchemy import SQLAlchemy
import somestuff

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:' + somestuff.mysql_pass + '@localhost/grocerylist'
db = SQLAlchemy(app)

class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), nullable=False)

class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    product_type = db.Column(db.String(30), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    description = db.Column(db.String(255))

    category = db.relationship("Category",
                            backref=('products'))

    def __init__(self,name, quantity, product_type, category_id, description):
        self.name = name
        self.quantity = quantity
        self.product_type = product_type
        self.category_id = category_id
        self.description = description

db.create_all()
db.session.commit()

app.config.update(dict(
    SECRET_KEY="super awesome key"
))

class MyForm(FlaskForm):
    name = StringField('Product name', validators=[InputRequired(), Length(min=1, max=30)])
    quantity = DecimalField('Quantity', validators=[InputRequired()])
    product_type = StringField('Product Type')
    category_id = DecimalField('Category')
    description = StringField("Description", validators=[Length(min=0, max=255)])

@app.route('/', methods=['GET', 'POST'])
def homepage():
    return render_template('homepage.html')

@app.route('/submit', methods=['GET', 'POST'])
def submit():
    form = MyForm()
    if form.validate_on_submit():
        if request.method == 'POST':
            new_product = Product(request.form['name'], request.form['quantity'], request.form['product_type'],
                                  request.form['category_id'], request.form['description'])
            db.session.add(new_product)
            db.session.commit()
            return render_template('/result_submit.html', form=form, new_product=new_product)
    return render_template('submit.html', form=form)

@app.route('/success', methods=['GET', 'POST'])
def success():
    return redirect('/success')

@app.route('/grocery-list', methods=['GET'])
def display_data():
    data = db.session.query(Product, Category).join(Category).all()
    return render_template('query_database.html', data=data)

# New list creation module
@app.route('/delete-data', methods=['GET', 'POST'])
def delete():
    deletion = Product.query.delete()
    db.session.commit()
    return render_template('delete_page.html', deletion=deletion)

@app.route('/created-new-list', methods=['GET', 'POST'])
def afterwards():
    reset =db.engine.execute("ALTER TABLE grocerylist.product AUTO_INCREMENT = 1;")
    return render_template('afterwards.html', reset=reset)

# deleting single item module
def find_name(erase, field):
    item = field.data
    data = db.session.query(db.exists().where(Product.name == item)).scalar()
    if data is False:
        raise ValidationError("There isn't any item with this name")
    else:
        something = db.session.query(Product).filter(Product.name == item).first()
        db.session.delete(something)
        db.session.commit()

class RemoveForm(FlaskForm):
    name = StringField('Product name', validators=[InputRequired(), find_name])

@app.route('/delete-item', methods=['GET', 'POST'])
def removal():
    erase = RemoveForm()
    data = db.session.query(Product).all()
    if request.method == 'POST':
        if erase.validate_on_submit():
            data = db.session.query(Product, Category).join(Category).all()
            return render_template('item_deleted.html', data=data)
    return render_template('delete_item.html', erase=erase, data=data)

# update item module
def search_for_name(update, field):
    """Checks if input exists in db"""
    item = field.data
    data = db.session.query(db.exists().where(Product.name == item)).scalar()
    if data is False:
        raise ValidationError("There isn't any item with this name")

class UpdateForm(FlaskForm):
    item_name = StringField('Product from the list', validators=[InputRequired(), search_for_name])
    name = StringField('New name', validators=[InputRequired(), Length(min=1, max=30)])
    quantity = DecimalField('Quantity', validators=[InputRequired()])
    product_type = StringField('Product Type')
    category_id = DecimalField('Category')
    description = StringField("Description", validators=[Length(min=0, max=255)])

@app.route('/update-item', methods=['GET', 'POST'])
def update():
    data = db.session.query(Product, Category).join(Category).all()
    update = UpdateForm()
    if request.method == 'POST':
        if update.validate_on_submit():
            something = db.session.query(Product).filter(Product.name == request.form['item_name']).update({'name' : request.form['name'],
                                                               'quantity' : request.form['quantity'],
                                                               'product_type' : request.form['product_type'],
                                                               'category_id' : request.form['category_id'],
                                                               'description' : request.form['description']})
            db.session.commit()
            return render_template('updated_item.html')
    return render_template('update_item.html', update=update, data=data)

if __name__ == "__main__":
    app.run(debug=True)