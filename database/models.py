import os
from datetime import datetime,timedelta
from sqlalchemy.orm import relationship
from database.utilities import db, Base, session
from logger import logger

DB_SCHEMA = os.getenv("DB_SCHEMA")


class User(Base):
    """
    TODO: Back reference
    """

    __tablename__ = "user_info"
    __table_args__ = {"schema": DB_SCHEMA}
    id = db.Column("id", db.Integer, primary_key=True)
    user_id = db.Column("user_id", db.String(255))
    name = db.Column("username", db.String(255))
    date = db.Column("date_created", db.DateTime, default=datetime.now())
    stamina = db.Column("stamina", db.Integer,default=3)
    points = db.Column("points", db.Integer, default=0)
    song_requests = relationship("SongRequests", backref="user", lazy=True)
    sound_effects = relationship("SoundEffects", backref="user", lazy=True)
    user_commands = relationship("UserCommands", backref="user", lazy=True)
    user_messages = relationship("UserMessages", backref="user", lazy=True)

    def save(self):
        first_row = session.query(User).filter_by(user_id=self.user_id).first()
        if first_row is None:
            session.add(self)
            session.commit()
            return self
        return first_row

    def __repr__(self):
        return "<User(userid={0})>".format(self.user_id)


class SoundEffects(Base):
    """
    TODO: Mana Limitation system.
    """

    __tablename__ = "sound_effects"
    __table_args__ = {"schema": DB_SCHEMA}
    id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column("sound_name", db.String(255))
    url = db.Column("sound_url", db.String(255))
    sound_type = db.Column("sound_type", db.String(255))
    sound_status = db.Column("sound_status", db.String(255),default="unapproved")
    start_time = db.Column("start_time", db.Integer)
    end_time = db.Column("end_time", db.Integer)
    user_id = db.Column(
        db.Integer, db.ForeignKey(f"{DB_SCHEMA}.user_info.id"), nullable=False
    )
    date = db.Column("date", db.DateTime, default=datetime.now())

    def save(self):
        first_row = session.query(SoundEffects).filter_by(user_id=self.user_id,name=self.name).first()
        if first_row is None:
            session.add(self)
            session.commit()
            return self
        return None


    def __repr__(self):
        return f"<SoundEffects(name={self.name},url={self.url},start={self.start_time},end={self.end_time})>"


class SongRequests(Base):
    """
    Request interval used to track times requested
    per unit of time. Can be reset and updated per unit
    of time.
    """

    __tablename__ = "song_requests"
    __table_args__ = {"schema": DB_SCHEMA}
    id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column("song_name", db.String(255))
    url = db.Column("song_url", db.String(255))
    status = db.Column("song_status", db.String(255))
    times_requested = db.Column("times_requested", db.Integer, default=1)
    request_interval = db.Column("request_interval", db.Integer, default=0)
    user_id = db.Column(
        db.Integer, db.ForeignKey(f"{DB_SCHEMA}.user_info.id"), nullable=False
    )
    date = db.Column("date_created", db.DateTime, default=datetime.now())
    last_requested = db.Column("date_modified", db.DateTime, default=datetime.now())

    def save(self):
        first_row = session.query(SongRequests).filter_by(url=self.url).first()
        if first_row is None:
            session.add(self)
            session.commit()
            return self
        first_row.last_requested = datetime.now()
        first_row.times_requested = first_row.times_requested + 1
        session.commit()
        return first_row

    def __repr__(self):
        return "<SongRequests(name={0})>".format(self.name)


class UserCommands(Base):
    """
    TODO: Add cooldowns
    """

    __tablename__ = "user_commands"
    __table_args__ = {"schema": DB_SCHEMA}
    id = db.Column("id", db.Integer, primary_key=True)
    command_name = db.Column("command_name", db.String(255))
    message = db.Column("message", db.String(255))
    aliases = db.Column("aliases", db.String(255))
    user_level = db.Column("user_level", db.String(255))
    user_id = db.Column(
        db.Integer, db.ForeignKey(f"{DB_SCHEMA}.user_info.id"), nullable=False
    )
    date = db.Column("date_created", db.DateTime, default=datetime.now())

    def __repr__(self):
        return "<UserCommands(date={0})>".format(self.date)


class UserMessages(Base):
    __tablename__ = "user_messages"
    __table_args__ = {"schema": DB_SCHEMA}
    id = db.Column("id", db.Integer, primary_key=True)
    message = db.Column("message", db.String(255))
    user_id = db.Column(
        db.Integer, db.ForeignKey(f"{DB_SCHEMA}.user_info.id"), nullable=False
    )
    date = db.Column("date_created", db.DateTime, default=datetime.now())

    @property
    def first_message(self):
        yesterday = datetime.today() - timedelta(days=1)
        messages = session.query(UserMessages).filter(UserMessages.date > yesterday).all()
        if len(messages) > 1:
            return False
        return True

    def save(self):
        first_row = (
            session.query(UserMessages)
            .filter_by(user_id=self.user_id, message=self.message)
            .first()
        )
        if first_row is None:
            session.add(self)
            session.commit()
            return self
        return first_row

    def __repr__(self):
        return "<UserMessage(date={0})>".format(self.date)
