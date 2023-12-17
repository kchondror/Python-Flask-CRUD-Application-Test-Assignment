from config.flask_init import request
from config.database_init import *
from data.models.Person_model import Person


@contextmanager
def db_session():
    """ Creates a context with an open SQLAlchemy session.
    """
    db_session = create_session()
    yield db_session
    db_session.close()


def calculate_pagination():

    page = request.args.get('page', 1, type=int)
    cards_per_page = 6
    start = (page - 1) * cards_per_page

    items = Read_DB(start)
    total_pages = (count_records() + cards_per_page - 1) // cards_per_page

    return items, total_pages, page


def Read_DB(offset):

    with db_session() as db:
        result = (
            db.query(Person)
            .offset(offset)
            .limit(6)
            .all()
        )
    return result


def count_records():
    with db_session() as db:
        result = db.query(Person).count()

    return result
