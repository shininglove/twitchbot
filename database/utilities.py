from logger import logger
from database.config import connection
import sqlalchemy as db
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

engine = db.create_engine(connection)

Session = sessionmaker()

Session.configure(bind=engine)

session = Session()


class Model:
    def save(self):
        try:
            session.add(self)
        except Exception as e:
            logger.debug(e)
        session.commit()


def create_table(model, engine=engine):
    if not model.__table__.exists(engine):
        model.__table__.create(engine)
        return "Created."
    return "Already exists."


def delete_table(model, engine=engine):
    if model.__table__.exists(engine):
        model.__table__.drop(engine)
        return "Deleted."
    return "Does not exist."


# print(create_table(TableName))
# print(create_table(TableFull))
# check_request = session.query(TableName).all()
# print(check_request)
