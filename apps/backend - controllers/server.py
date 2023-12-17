from config.flask_init import *
import database_condroller as db


@app.route('/', methods=["GET", "POST"])
def home_page():

    items_on_page, total_pages, page = db.calculate_pagination()

    return render_template("index.html", people=items_on_page, total_pages=total_pages, page=page)


@app.route('/insertion', methods=["GET", "POST"])
def insertion_page():
    return render_template("insertion.html")


if __name__ == "__main__":
    app.run(debug=True)
