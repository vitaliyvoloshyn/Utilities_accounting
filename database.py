import os
from typing import Type

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import DeclarativeBase
from dotenv import load_dotenv
from utilities_accounting.models import Base
from utilities_accounting.testing_data import add_data, my_select


class DB:

    def __init__(self, base: Type[DeclarativeBase], echo: bool = False):
        self.__get_environ()
        self.engine = create_engine(
            f"postgresql+psycopg2://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}",
            echo=True)
        self.session = sessionmaker(self.engine)
        self.Base = base

    def create_db(self):
        self.Base.metadata.create_all(self.engine)

    def drop_db(self):
        print(self.engine)
        self.Base.metadata.drop_all(self.engine)

    def insert_test_data(self):
        add_data(self.session)
        my_select(self.session)


    def get_session(self):
        return self.session

    def __get_environ(self):
        self.db_user = os.environ.get('DB_USER')
        self.db_password = os.environ.get('DB_PASSWORD')
        self.db_host = os.environ.get('DB_HOST')
        self.db_port = os.environ.get('DB_PORT')
        self.db_name = os.environ.get('DB_NAME')


load_dotenv()
db = DB(Base, True)


def get_db():
    return db
