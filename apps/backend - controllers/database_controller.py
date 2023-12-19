from config.flask_init import request
from config.database_init import *
from data.models.Person_model import Person
import requests


@contextmanager
def db_session() -> None:
    """
    Creates a context manager that provides an open SQLAlchemy session and
    closes it when the context is exited.
    """
    session = create_session()
    yield session
    session.close()


def calculate_pagination(search_string: str | None = None) -> tuple[list, int, int]:
    """
    Calculates pagination for a search query.
    If the search string is provided, the function will perform a search using the search
    string parameter and return the matching items.
    If the search string is not provided, the function will return
    a subset of records from the database
    
    :param search_string: A string that is used to search for specific items in the database.

    :return: three values: "items": a list of sql-alchemy rows,
    "total_pages": an integer for the total pages of the content, and
    "page": an integer for the current page.
    """
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


def CreateRecord(form_data: dict) -> tuple[str, str]:
    """
    Creates a new record in a database table using the provided form data,
    and returns a success message if the record is added successfully, or an error message if there is
    an issue.
    
    :param form_data: A dictionary that contains the data submitted through
    a form.

    :return: a tuple containing two values.
    A string message indicating the result of the operation.
    A string indicating the type of message.
    """
    with db_session() as db:
        try:
            sql = text(
                "INSERT INTO person_table (firstName, lastName, email, phoneNumber, address) "
                "VALUES (:firstName, :lastName, :email, :phoneNumber, :address) ") \
                .bindparams(
                firstName=form_data["first_name"],
                lastName=form_data["last_name"],
                email=form_data["email"],
                phoneNumber=form_data["phone_number"],
                address=form_data["address"])

            db.execute(sql)
            db.commit()
        except IntegrityError:
            db.rollback()
            return "This Email Already Exists!", "warning"
        except SQLAlchemyError:
            db.rollback()
            return "Something Went Wrong!", "warning"

    return "New Person Added to the Database!", "success"


def ReadRecords(offset: int, limit: int) -> list:
    """
    Retrieves a specified number of records from a database table, starting from a given offset.
    
    :param offset: The starting point of the records to be retrieved from the person_table.
    :param limit: The maximum number of records to retrieve from the person_table.

    :return: a list of sql-alchemy rows.
    """
    with db_session() as db:
        sql = text(
            "SELECT * "
            "FROM person_table "
            "LIMIT :lim OFFSET :off ").bindparams(lim=limit, off=offset)

        result = db.execute(sql).all()

    return result


def UpdateRecord(form_data: dict, Id: int) -> tuple[str, str]:
    """
    Updates a record in the person_table with the provided form data.
    
    :param form_data: A dictionary that contains the updated values for the record
    :param Id: The unique identifier of the record that needs to be updated in th person_table.

    :return: a tuple containing two values.
    A string message indicating the result of the operation.
    A string indicating the type of message.
    """
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


def DeleteRecord(Id: int) -> tuple[str, str]:
    """
    Deletes a record from the person_table in a database using the provided Id.
    
    :param Id: The unique identifier of the record that you want to delete from the person_table.

    :return: a tuple containing two values.
    A string message indicating the result of the operation.
    A string indicating the type of message.
    """
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


def Search(search_string: str) -> list:
    """
    Takes a search string as input, splits it into individual words, and searches
    a database for records that match any of the words in the search string.
    
    :param search_string: A string that contains the keywords or terms that you want to search for in the person_table

    :return: a list of sql-alchemy rows.
    """
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


def GetPerson(Id: int) -> list:
    """
    Retrieves a person's information from a database based on their ID.
    
    :param Id: The unique identifier of the person you want to retrieve from the person_table.

    :return: a list of sql-alchemy rows (one).
    """
    with db_session() as db:
        sql = text(
            "SELECT * "
            "FROM person_table "
            "WHERE Id = :id").bindparams(id=Id)
        result = db.execute(sql).all()

    return result


def count_records() -> int:
    """
    Counts the number of records in the person_table.

    :return: an integer for the count of records.
    """
    with db_session() as db:
        result = db.query(Person).count()

    return result


if __name__ == "__main__":
    """This code block provides a way to add data to the database using the random user generator site(
    "https://randomuser.me/"). """
    for i in range(15):
        fake_person = requests.get('https://randomuser.me/api/').json()['results'][0]

        data = {"first_name": fake_person['name']['first'],
                "last_name": fake_person['name']['last'],
                "email": fake_person['email'],
                "phone_number": fake_person['phone'],
                "address": f"{fake_person['location']['street']['name']} "
                           f"{fake_person['location']['street']['number']}"}
        CreateRecord(data)
