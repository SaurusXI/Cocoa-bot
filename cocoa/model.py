from datetime import time

from sqlalchemy import create_engine
from sqlalchemy import Column, String, Integer, Time
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
    StartTime = Column(Time, primary_key = True)
    EndTime = Column(Time, primary_key = True)


session = sessionmaker(db)()
base.metadata.create_all(db)


def create_meeting(uid1: int, uid2: int):
    meeting = Meeting(UID1 = uid1, UID2 = uid2)
    session.add(meeting)
    session.commit()

def delete_meeting(uid1: int, uid2: int):
    meeting = session.query(Meeting).get((uid1, uid2))
    session.delete(meeting)
    session.commit()

def create_user(uid: int, description: str):
    user = User(UID = uid, Description = description)
    session.add(user)
    session.commit()

def read_user(uid: int):
    user = session.query(User).get(uid)
    return user

def update_user(uid: int, description: str):
    user = read_user(uid)
    user.Description = description
    session.commit()

def delete_user(uid: int):
    user = read_user(uid)from datetime import time
    session.delete(user)
    session.commit()

def create_schedule(uid: int, start: time, end: time):
    schedule = Schedule(UID = uid, StartTime = start, EndTime = end)
    session.add(schedule)
    session.commit()

def get_user_schedules(uid: int):
    schedules = session.query(Schedule).filter(Schedule.UID == uid)
    return schedules

def read_schedule(uid: int, start: time, end: time):
    schedule = session.query(Schedule).get((uid, start, end))
    return schedule

def update_schedule(uid: int, prevstart: time, prevend: time, newstart: time, newend: time):
    schedule = read_schedule(uid, prevstart, prevend)
    schedule.StartTime = newstart
    schedule.EndTime = newend
    session.commit()

def delete_schedule(uid: int, start: time, end: time):
    schedule = read_schedule(uid, start, end)
    session.delete(schedule)
    session.commit()
