from config.database_init import *

_BASE_CLASS = declarative_base()


class Person(_BASE_CLASS):
    __tablename__ = "person_table"

    Id = Column("Id", Integer, primary_key=True)
    firstName = Column("firstName", String(22), nullable=False)
    lastName = Column("lastName", String(22), nullable=False)
    email = Column("email", String(255), nullable=False, unique=True)
    phoneNumber = Column("phoneNumber", VARCHAR(50), nullable=False)
    address = Column("address", String(255))

    def __init__(self, firstName, lastName, email, phoneNumber, address=None):
        self.firstName = firstName
        self.lastName = lastName
        self.email = email
        self.phoneNumber = phoneNumber
        self.address = address

if __name__ == "__main__":
    _BASE_CLASS.metadata.create_all(bind=ENGINE)
