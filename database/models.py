import os
from datetime import datetime
from utilities import db, Base

DB_SCHEMA = os.getenv("DB_SCHEMA")

class User(Base):
    __tablename__ = "user_info"
    __table_args__ = {'schema': DB_SCHEMA}
    id = db.Column("id", db.Integer, primary_key=True)
    user_id = db.Column("user_id", db.String(255))
    name = db.Column("username", db.String(255))
    date = db.Column("date_created", db.DateTime, default=datetime.now())

    def __repr__(self):
        return "<User(userid={0})>".format(self.user_id)

class SoundEffects(Base):
    __tablename__ = "sound_effects"
    __table_args__ = {'schema': DB_SCHEMA}
    id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column("sound_name", db.String(255))
    url = db.Column("sound_url", db.String(255))
    sound_type = db.Column("sound_type", db.String(255))
    start_time = db.Column("start_time", db.Integer)
    end_time = db.Column("end_time", db.Integer)
    user_id = db.Column(db.Integer,db.ForeignKey(f"{DB_SCHEMA}.user_info.id"),nullable=False)
    date = db.Column("date", db.DateTime, default=datetime.now())

    def __repr__(self):
        return "<SoundEffects(name={0})>".format(self.name)


class SongRequests(Base):
    __tablename__ = "song_requests"
    __table_args__ = {'schema': DB_SCHEMA}
    id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column("song_name", db.String(255))
    url = db.Column("song_url", db.String(255))
    status = db.Column("song_status", db.String(255))
    times_requested = db.Column("times_requested", db.Integer, default=0)
    user_id = db.Column(db.Integer,db.ForeignKey(f"{DB_SCHEMA}.user_info.id"),nullable=False)
    date = db.Column("date_created", db.DateTime, default=datetime.now())
    last_requested = db.Column("date_modified", db.DateTime, default=datetime.now())

    def __repr__(self):
        return "<SongRequests(name={0})>".format(self.name)

class UserCommands(Base):
    __tablename__ = "user_commands"
    __table_args__ = {'schema': DB_SCHEMA}
    id = db.Column("id", db.Integer, primary_key=True)
    command_name = db.Column("command_name", db.String(255))
    message = db.Column("message", db.String(255))
    aliases = db.Column("aliases", db.String(255))
    user_id = db.Column(db.Integer,db.ForeignKey(f"{DB_SCHEMA}.user_info.id"),nullable=False)
    date = db.Column("date_created", db.DateTime, default=datetime.now())

    def __repr__(self):
        return "<UserMessage(date={0})>".format(self.date)

class UserMessages(Base):
    __tablename__ = "user_messages"
    __table_args__ = {'schema': DB_SCHEMA}
    id = db.Column("id", db.Integer, primary_key=True)
    message = db.Column("message", db.String(255))
    user_level = db.Column("user_level", db.String(255))
    user_id = db.Column(db.Integer,db.ForeignKey(f"{DB_SCHEMA}.user_info.id"),nullable=False)
    date = db.Column("date_created", db.DateTime, default=datetime.now())

    def __repr__(self):
        return "<UserMessage(date={0})>".format(self.date)

