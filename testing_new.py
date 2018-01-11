from flask import Flask
from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, validators, SubmitField
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

#figure it out!!!!
@app.route('/success', methods=['GET', 'POST'])
def success():
    form = MyForm()
    return redirect('/success')

@app.route('/grocery-list', methods=['GET'])
def display_data():
    data = db.session.query(Product, Category).join(Category).all()
    return render_template('query_database.html', data=data)



if __name__ == "__main__":
    app.run(debug=True)