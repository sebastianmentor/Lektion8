from flask_wtf import FlaskForm
from wtforms import Form, StringField, validators


class KontaktaOssForm(FlaskForm):
    name = StringField("name", [validators.Length(min=2,max=666)])
    email = StringField("email")
    text = StringField("text")