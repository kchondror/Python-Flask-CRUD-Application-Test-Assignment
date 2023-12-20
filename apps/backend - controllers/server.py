import sys, os

_dirname = os.path.dirname
_ROOT_DIR = _dirname(_dirname(_dirname(os.path.abspath(__file__))))

sys.path.append(_ROOT_DIR)

from config.flask_init import *
import database_controller as db
from data.models.insertion_form import InsertionForm
from wtforms import Label


@app.route('/', methods=["GET", "POST"])
def home_page() -> str:
    """
    A Flask route function that handles both GET and POST requests for the home page, including
    pagination and search functionality.
    If the method is "POST", it checks if there is a search string in the form data. If there
    is, it calculates pagination based on the search string and returns a rendered template with the
    search results.
    If the method is not "POST" or there is no search string, it calculates pagination
    for the whole database.

    :return: the rendered template "index.html" along with items_on_page, total_pages, page, isSearch variables.
    """
    if request.method == "POST":
        search_string = request.form['search_bar']
        if search_string:
            items_on_page, total_pages, page = db.calculate_pagination(search_string)
            return render_template("index.html", people=items_on_page, total_pages=total_pages, page=page,
                                   isSearch=True)

    items_on_page, total_pages, page = db.calculate_pagination()
    return render_template("index.html", people=items_on_page, total_pages=total_pages, page=page, isSearch=False)


@app.route('/insertion', methods=["GET", "POST"])
def insertion_page() -> str:
    """
    Handles the insertion page, where users can input data and submit it to be stored in
    the database.

    :return: the rendered template "insertion.html" along with the form object.
    """
    form = InsertionForm()
    if request.method == "POST" and form.validate_on_submit():
        message, category = db.CreateRecord(form.data)
        print(type(form.data))
        flash(message, category=category)

        return redirect(url_for('insertion_page'))

    return render_template("insertion.html",
                           form=form)


@app.route('/update/<int:Id>', methods=["GET", "POST"])
def update(Id: int) -> str:
    """
    Handles the updating of a record in a database based on the provided ID.

    :param Id: The unique identifier of the record that needs to be updated.

    :return: the rendered template "update.html" with the form object.
    """
    form = InsertionForm()

    if request.method == "POST" and form.validate():
        message, category = db.UpdateRecord(form.data, Id)
        flash(message, category=category)

        return redirect(url_for('home_page'))

    result = db.GetPerson(Id)[0]

    fields = ['first_name', 'last_name', 'email', 'phone_number', 'address']
    for field, value in zip(fields, result[1:6]):
        form[field].default = value

    form.save_button.label = Label(form.save_button.id, 'Update')
    form.process()

    return render_template("update.html", form=form)


@app.route('/delete/<int:Id>')
def delete(Id: int) -> str:
    """
    Deletes a record from the database based on the given Id.

    :param Id: The unique identifier of the record that needs to be deleted.

    :return: a redirect to the 'home_page' route after deleting a record.
    """
    message, category = db.DeleteRecord(Id)
    flash(message, category=category)

    return redirect(url_for('home_page'))


if __name__ == "__main__":
    app.run()
