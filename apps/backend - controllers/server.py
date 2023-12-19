from config.flask_init import *
import database_controller as db
from data.models.insertion_form import InsertionForm
from wtforms import Label


@app.route('/update/<int:id>', methods=["GET", "POST"])
def update(id):
    form = InsertionForm()

    if request.method == "POST":
        message, category = db.UpdateRecord(form.data, id)
        flash(message, category=category)

        return redirect(url_for('home_page'))

    result = db.GetPerson(id)

    form.first_name.default = result[0][1]
    form.last_name.default = result[0][2]
    form.email.default = result[0][3]
    form.phone_number.default = result[0][4]
    form.address.default = result[0][5]
    form.save_button.label = Label(form.save_button.id, 'Update')

    form.process()

    return render_template("update.html", form=form)


@app.route('/delete/<int:id>')
def delete(id):
    message, category = db.DeleteRecord(id)
    flash(message, category=category)

    return redirect(url_for('home_page'))


@app.route('/', methods=["GET", "POST"])
def home_page():
    items_on_page, total_pages, page = db.calculate_pagination()

    return render_template("index.html", people=items_on_page, total_pages=total_pages, page=page)


@app.route('/insertion', methods=["GET", "POST"])
def insertion_page():
    form = InsertionForm()
    if request.method == "POST":
        message, category = db.CreateRecord(form.data)
        flash(message, category=category)

        return redirect(url_for('insertion_page'))

    return render_template("insertion.html",
                           form=form)


if __name__ == "__main__":
    app.run(debug=True)
