from config.flask_init import *
import database_controller as db
from data.models.insertion_form import InsertionForm


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
