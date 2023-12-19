from lib.wtForms_imports import *


class InsertionForm(FlaskForm):
    """
    This class inherits from FlaskForm of the flask-wtf module and declares an html form with validation and CSRF
    protection.
    """
    first_name: str = StringField("First Name", validators=[DataRequired()], render_kw={"placeholder": "First name"})
    last_name: str = StringField("Last Name", validators=[DataRequired()], render_kw={"placeholder": "Last name"})
    email: EmailField = EmailField("Email", validators=[validators.Email(), DataRequired()], render_kw={"placeholder": "Email"})
    phone_number: str = StringField("Phone", validators=[DataRequired()])
    address: str = StringField("Address", validators=None)

    save_button: SubmitField = SubmitField("Add Person", validators=None)
