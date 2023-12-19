from config.database_init import *

_BASE_CLASS = declarative_base()


class Person(_BASE_CLASS):
    """
    This class inherits from the declarative_base() base class of the SQLAlchemy module and instantiates the
    "person_table" model used in the sqlite database used in the application.
    """
    __tablename__: str = "person_table"

    Id: Column[int] = Column("Id", Integer, primary_key=True)
    firstName: Column[str] = Column("firstName", String(22), nullable=False)
    lastName: Column[str] = Column("lastName", String(22), nullable=False)
    email: Column[str] = Column("email", String(255), nullable=False, unique=True)
    phoneNumber: Column[VARCHAR] = Column("phoneNumber", VARCHAR(50), nullable=False)
    address: Column[str] = Column("address", String(255))

    def __init__(self, firstName, lastName, email, phoneNumber, address=None) -> None:
        self.firstName = firstName
        self.lastName = lastName
        self.email = email
        self.phoneNumber = phoneNumber
        self.address = address


if __name__ == "__main__":
    _BASE_CLASS.metadata.create_all(bind=ENGINE)
