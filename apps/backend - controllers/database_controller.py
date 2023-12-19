from config.flask_init import request
from config.database_init import *
from data.models.Person_model import Person
import requests


@contextmanager
def db_session():
    """ Creates a context with an open SQLAlchemy session.
    """
    session = create_session()
    yield session
    session.close()


def calculate_pagination(search_string=None):
    page = request.args.get('page', 1, type=int)
    cards_per_page = 6
    offset = (page - 1) * cards_per_page

    if search_string is None:

        items = ReadRecords(offset, cards_per_page)
        total_records = count_records()
    else:
        items = Search(search_string)
        total_records = len(items)

    total_pages = (total_records + cards_per_page - 1) // cards_per_page

    return items, total_pages, page


def CreateRecord(form_data):
    record = Person(firstName=form_data["first_name"],
                    lastName=form_data["last_name"],
                    email=form_data["email"],
                    phoneNumber=form_data["phone_number"],
                    address=form_data["address"])

    with db_session() as db:
        try:
            db.add(record)
            db.commit()
        except IntegrityError:
            db.rollback()
            return "This Email Already Exists!", "warning"
        except SQLAlchemyError:
            db.rollback()
            return "Something Went Wrong!", "warning"

    return "New Person Added to the Database!", "success"


def ReadRecords(offset, limit):
    with db_session() as db:
        sql = text(
            "SELECT * "
            "FROM person_table "
            "LIMIT :lim OFFSET :off ").bindparams(lim=limit, off=offset)

        result = db.execute(sql).all()

    return result


def UpdateRecord(form_data, Id):
    with db_session() as db:
        try:
            sql = text(
                "UPDATE person_table "
                "SET firstName = :firstName, lastName = :lastName, email = :email,"
                "phoneNumber = :phoneNumber,address = :address "
                "WHERE Id = :id").bindparams(id=Id, firstName=form_data["first_name"], lastName=form_data["last_name"],
                                             email=form_data["email"], phoneNumber=form_data["phone_number"],
                                             address=form_data["address"])

            db.execute(sql)
            db.commit()
        except IntegrityError:
            db.rollback()
            return "This Email Already Exists!", "warning"
        except SQLAlchemyError:
            db.rollback()
            return "Something Went Wrong", "warning"

    return "Record Updated Successfully!", "success"


def DeleteRecord(Id):
    with db_session() as db:
        try:
            sql = text(
                "DELETE FROM person_table "
                "WHERE Id = :id").bindparams(id=Id)

            db.execute(sql)
            db.commit()
        except SQLAlchemyError:
            db.rollback()
            return "Something Went Wrong!", "warning"
    return "Record Deleted Successfully!", "danger"


def Search(search_string):
    result_list = []
    search_list = search_string.split()

    with db_session() as db:
        for word in search_list:
            sql = text(
                "SELECT * "
                "FROM person_table "
                "WHERE (firstName || ' ' || lastName) LIKE :pattern"
            ).bindparams(pattern=f'%{word}%')

            result = db.execute(sql).all()
            result_list.extend(row for row in result)

    return result_list


def GetPerson(Id):
    with db_session() as db:
        sql = text(
            "SELECT * "
            "FROM person_table "
            "WHERE Id = :id").bindparams(id=Id)
        result = db.execute(sql).all()

    return result


def count_records():
    with db_session() as db:
        result = db.query(Person).count()

    return result


if __name__ == "__main__":

    for i in range(15):
        fake_person = requests.get('https://randomuser.me/api/').json()['results'][0]

        data = {"first_name": fake_person['name']['first'],
                "last_name": fake_person['name']['last'],
                "email": fake_person['email'],
                "phone_number": fake_person['phone'],
                "address": f"{fake_person['location']['street']['name']} "
                           f"{fake_person['location']['street']['number']}"}
        CreateRecord(data)
