from flask import Flask
from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, validators, SubmitField
from flask import render_template, redirect, url_for, request
from wtforms.validators import InputRequired, Length
from flask_sqlalchemy import SQLAlchemy
import enum
import somestuff

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:' + somestuff.mysql_pass + '@localhost/grocerylist'
db = SQLAlchemy(app)


class MyEnum(enum.Enum):
    piece = "piece"
    kg = "kg"

class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), nullable=False)

class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    product_type = db.Column(db.Enum(MyEnum), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    description = db.Column(db.String(255))

    category = db.relationship("Category",
                            backref=('products'))

db.create_all()
db.session.commit()


app.config.update(dict(
    SECRET_KEY="super awesome key"
))

class MyForm(FlaskForm):
    name = StringField('Product name', validators=[InputRequired(), Length(min=1, max=30)])
    product_quantity = DecimalField('Quantity', validators=[InputRequired()])
    product_type = StringField('Product Type')
    category = StringField('Category')
    description = StringField("Description", validators=[Length(min=0, max=255)])

@app.route('/', methods=['GET', 'POST'])
def index():
    form = MyForm()
    if form.validate_on_submit():
        return redirect(url_for('success'))
    return render_template('submit.html', form=form)


@app.route('/success')
def success():
    return render_template('result_submit.html')

if __name__ == "__main__":
    app.run(debug=True)