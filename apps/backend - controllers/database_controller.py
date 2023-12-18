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


def CreateRecord(data):
    record = Person(firstName=data["first_name"],
                    lastName=data["last_name"],
                    email=data["email"],
                    phoneNumber=data["phone_number"],
                    address=data["address"])

    with db_session() as db:
        try:
            db.add(record)
            db.commit()
        except IntegrityError:
            db.rollback()
            return ("This email already exists", "warning")
        except SQLAlchemyError:
            db.rollback()
            return ("Something went wrong", "warning")

    return ("New person added to the database", "success")


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
            return ("Something went wrong", "warning")
    return ("Record Deleted Successfully", "danger")


def count_records():
    with db_session() as db:
        result = db.query(Person).count()

    return result
