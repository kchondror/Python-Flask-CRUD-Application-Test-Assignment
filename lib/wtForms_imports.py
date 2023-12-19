from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, IntegerField, SubmitField, validators
from wtforms.validators import DataRequired, Regexp
import email_validator
