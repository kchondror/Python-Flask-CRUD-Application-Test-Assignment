from config.flask_init import request
from config.database_init import *
from data.models.Person_model import Person


@contextmanager
def db_session():
    """ Creates a context with an open SQLAlchemy session.
    """
    session = create_session()
    yield session
    session.close()


def calculate_pagination():
    page = request.args.get('page', 1, type=int)
    cards_per_page = 6
    offset = (page - 1) * cards_per_page

    items = ReadRecords(offset, cards_per_page)
    total_pages = (count_records() + cards_per_page - 1) // cards_per_page

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
            "LIMIT :lim OFFSET :off").bindparams(lim=limit, off=offset)
        result = db.execute(sql).all()

    return result


def DeleteRecord(id):
    with db_session() as db:
        try:
            sql = text(
                "DELETE FROM person_table "
                "WHERE Id = :id").bindparams(id=id)

            db.execute(sql)
            db.commit()
        except SQLAlchemyError:
            db.rollback()
            return "Something Went Wrong!", "warning"
    return "Record Deleted Successfully!", "danger"


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
        data = {"first_name": 'test',
                "last_name": i,
                "email": f"test{i}@mail.com",
                "phone_number": 1234,
                "address": f"test address {i}"}
        CreateRecord(data)
