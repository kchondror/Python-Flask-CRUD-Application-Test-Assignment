from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, IntegerField, SubmitField, validators
from wtforms.validators import DataRequired
import email_validator
