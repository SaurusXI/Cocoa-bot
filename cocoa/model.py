from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base  
from sqlalchemy.orm import sessionmaker

db_string = "postgres://user:mysecretpassword@host/dbname"
db = create_engine(db_string)
base = declarative_base()


class Meeting(base):
    __tablename__ = 'meetings'

    UID1 = Column(Integer, primary_key = True)
    UID2 = Column(Integer, primary_key = True)


class User(base):
    __tablename__ = 'users'

    UID = Column(Integer, primary_key = True)
    Description = Column(String)


class Schedule(base):
    __tablename__ = 'schedules'

    UID = Column(Integer, primary_key = True)
    StartTime = Column(DateTime, primary_key = True)
    EndTime = Column(DateTime, primary_key = True)



class ModelService:
    def __init__(self):
        self.session = sessionmaker(db)()
        base.metadata.create_all(db)

    def add_meeting(self, uid1: int, uid2: int):
        meeting = Meeting(UID1 = uid1, UID2 = uid2)
        self.session.add(meeting)
        self.session.commit()

    def delete_meeting(self, uid1: int, uid2: int):
        meeting = self.session.query(Meeting).get((uid1, uid2))
        self.session.delete(meeting)
        self.session.commit()

    def add_user(self, uid: int, description: str):
        user = User(UID = uid, Description = description)
        self.session.add(user)
        self.session.commit()

    def read_user(self, uid: int):
        user = self.session.query(User).get(uid)
        return user

    def update_user(self, uid: int, description: str):
        user = read_user(uid)
        user.Description = description
        self.session.commit()

    def delete_user(self, uid: int):
        user = read_user(uid)
        self.session.delete(user)
        self.session.commit()

    def add_schedule(self, uid: int, start: datetime, end: datetime):
        schedule = Schedule(UID = uid, StartTime = start, EndTime = end)
        self.session.add(schedule)
        self.session.commit()

    def get_user_schedules(self, uid: int):
        schedules = self.session.query(Schedule).filter(Schedule.UID == uid)
        return schedules

    def read_schedule(self, uid: int, start: datetime, end: datetime):
        schedule = self.session.query(Schedule).get((uid, start, end))
        return schedule

    def update_schedule(self, uid: int, prevstart: datetime, prevend: datetime, newstart: datetime, newend: datetime):
        schedule = read_schedule(uid, prevstart, prevend)
        schedule.StartTime = newstart
        schedule.EndTime = newend
        self.session.commit()

    def delete_schedule(self, uid: int, start: datetime, end: datetime):
        schedule = read_schedule(uid, start, end)
        self.session.delete(schedule)
        self.session.commit()
