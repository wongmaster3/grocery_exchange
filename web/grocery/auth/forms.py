from flask_wtf import FlaskForm
from wtforms import StringField, FloatField
from wtforms.validators import DataRequired, Email

class LoginForm(FlaskForm):
    log_name = StringField('log_name', validators=[DataRequired()])
    log_code = StringField('log_code', validators=[DataRequired()])


class RegisterForm(FlaskForm):
    reg_name = StringField('reg_name', validators=[DataRequired()])
    reg_code = StringField('reg_code', validators=[DataRequired()])
    reg_tax = StringField('reg_tax', validators=[DataRequired()])
    reg_tip = StringField('reg_tip', validators=[DataRequired()])
