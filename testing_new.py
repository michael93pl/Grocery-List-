from flask import Flask, request
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
from flask import render_template
from flask import redirect


app = Flask(__name__)


class MyForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])


app.config.update(dict(
    SECRET_KEY="super awesome key",
    WTF_CSRF_SECRET_KEY="crsf secret key"
))


@app.route('/submit', methods=['GET', 'POST'])
def submit():
    form = MyForm()
    if form.validate_on_submit():
        return redirect('/success')
    return render_template('submit.html', form=form)


if __name__ == "__main__":
    app.run()