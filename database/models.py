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
    user_id = db.Column(db.Integer,db.ForeignKey("user_info.id"),nullable=False)
    date = db.Column("date", db.DateTime, default=datetime.now())

    def __repr__(self):
        return "<SoundEffects(userid={0})>".format(self.user_id)


class SongRequests(Base):
    __tablename__ = "sound_requests"
    __table_args__ = {'schema': DB_SCHEMA}
    id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column("song_name", db.String(255))
    url = db.Column("song_url", db.String(255))
    status = db.Column("song_status", db.String(255))
    times_requested = db.Column("times_requested", db.Integer, default=0)
    user_id = db.Column(db.Integer,db.ForeignKey("user_info.id"),nullable=False)
    date = db.Column("date_created", db.DateTime, default=datetime.now())
    last_requested = db.Column("date_modified", db.DateTime, default=datetime.now())

    def __repr__(self):
        return "<SongRequests(userid={0})>".format(self.user_id)

class UserCommands(Base):
    pass
