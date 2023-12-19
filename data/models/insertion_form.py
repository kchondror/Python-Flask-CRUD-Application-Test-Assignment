from lib.wtForms_imports import *


class InsertionForm(FlaskForm):
    first_name = StringField("First Name", validators=[DataRequired()], render_kw={"placeholder": "First name"})
    last_name = StringField("Last Name", validators=[DataRequired()], render_kw={"placeholder": "Last name"})
    email = EmailField("Email", validators=[validators.Email(), DataRequired()], render_kw={"placeholder": "Email"})
    phone_number = StringField("Phone", validators=[DataRequired()])
    address = StringField("Address", validators=None)

    save_button = SubmitField("Add Person", validators=None)
