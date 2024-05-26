# models.py
from sqlalchemy import create_engine, Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Email(Base):
    """
    This is the Email model class which maps to the 'emails' table in the database.

    Attributes:
        __tablename__ (str): The name of the table in the database.
        id (Column): The primary key column of the table, which stores the email id.
        from_address (Column): The column that stores the sender's email address.
        subject (Column): The column that stores the subject of the email.
        received_date (Column): The column that stores the date and time the email was received.
    """
    __tablename__ = 'emails'
    id = Column(String(255), primary_key=True)  # Specify the length (e.g., 255)
    from_address = Column(String(255))
    subject = Column(String(255))
    received_date = Column(DateTime)


def get_session():
    engine = create_engine('mysql+pymysql://emailuser:rahul123@localhost/emaildb')  # Replace 'emailuser' and 'rahul123' with your actual user and password
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()
