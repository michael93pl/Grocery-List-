from flask import Flask
from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, validators
from flask import render_template


app = Flask(__name__)

app.config.update(dict(
    SECRET_KEY="super awesome key"
))


class MyForm(FlaskForm):
    name = StringField('Product name', [validators.InputRequired(), validators.Length(min=0, max=30)])
    product_quantity = DecimalField('Quantity', [validators.InputRequired()])
    category = StringField('Category', [validators.InputRequired()])
    product_type = StringField('Product Type', [validators.InputRequired()])



@app.route('/', methods=['GET', 'POST'])
def index():
    form = MyForm()
    if form.validate_on_submit():
        return "Mission accomplished!"
    return render_template('submit.html', form=form)


if __name__ == "__main__":
    app.run(debug=True)