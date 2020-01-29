from flask_wtf import FlaskForm
from wtforms import StringField, FieldList, FormField, FloatField, FileField
from wtforms.validators import DataRequired, Email

class ItemsEntryForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    price = FloatField('price', validators=[DataRequired()])
    split = FloatField('split', validators=[DataRequired()])


class FileForm(FlaskForm):
    file = FileField('file', validators=[DataRequired()])

