from datetime import datetime, timedelta

from sqlalchemy import create_engine
from sqlalchemy import and_, or_
from sqlalchemy import Column, String, DateTime, BigInteger
from sqlalchemy.ext.declarative import declarative_base  
from sqlalchemy.orm import sessionmaker

from cocoa.helpers import envloader

db_string = envloader.config.SQLALCHEMY_DATABASE_URL
db = create_engine(db_string)
base = declarative_base()


# Declare tables
# Meeting TABLE
class Meeting(base):
    __tablename__ = 'meetings'

    UID1 = Column(BigInteger, primary_key=True)
    UID2 = Column(BigInteger, primary_key=True)
    StartTime = Column(DateTime, primary_key=True)
    EndTime = Column(DateTime, primary_key=True)


# User TABLE
class User(base):
    __tablename__ = 'users'

    UID = Column(BigInteger, primary_key=True)
    Description = Column(String)
    Username = Column(String)


# Schedule TABLE
class Schedule(base):
    __tablename__ = 'schedules'

    UID = Column(BigInteger, primary_key=True)
    StartTime = Column(DateTime, primary_key=True)
    EndTime = Column(DateTime, primary_key=True)


# Main model class
class ModelService:
    def __init__(self):
        self.session = sessionmaker(db)()
        base.metadata.create_all(db)

    # Operations for Meeting
    def add_meeting(self, uid1: int, uid2: int, start: datetime, end: datetime):
        meeting = Meeting(UID1=uid1, UID2=uid2, StartTime=start, EndTime=end)
        self.session.add(meeting)
        self.session.commit()

    def delete_meeting(self, uid1: int, uid2: int):
        meeting = self.session.query(Meeting).get((uid1, uid2))
        self.session.delete(meeting)
        self.session.commit()

    def get_meetings(self, uid: int):
        meetings = self.session.query(Meeting).get(uid)
        result = []
        for meeting in meetings.all():
            result.append({
                'user1': meeting.UID1,
                'user2': meeting.UID2,
                'start': meeting.StartTime,
                'end': meeting.EndTime,
            })

        return result

    # Operations for User
    def add_user(self, uid: int, username: str, description: str):
        user = User(UID=uid, Username=username, Description=description)
        self.session.add(user)
        self.session.commit()

    def read_user(self, uid: int):
        user = self.session.query(User).get(uid)
        return user

    def update_user(self, uid: int, description: str):
        user = self.read_user(uid)
        user.Description = description
        self.session.commit()

    def delete_user(self, uid: int):
        user = self.read_user(uid)
        self.session.delete(user)
        self.session.commit()

    # Operations for Schedule
    def add_schedule(self, uid: int, start: datetime, end: datetime):
        schedule = Schedule(UID=uid, StartTime=start, EndTime=end)
        self.session.add(schedule)
        self.session.commit()

    def get_user_schedules(self, uid: int):
        schedules = self.session.query(Schedule).filter(Schedule.UID == uid)
        return schedules

    def read_schedule(self, uid: int, start: datetime, end: datetime):
        schedule = self.session.query(Schedule).get((uid, start, end))
        return schedule

    def update_schedule(self, uid: int, prevstart: datetime, prevend: datetime, newstart: datetime, newend: datetime):
        schedule = self.read_schedule(uid, prevstart, prevend)
        schedule.StartTime = newstart
        schedule.EndTime = newend
        self.session.commit()

    def delete_schedule(self, uid: int, start: datetime, end: datetime):
        schedule = self.read_schedule(uid, start, end)
        print(f'Schedule: {schedule}')
        self.session.delete(schedule)
        self.session.commit()

    def find_meetings(self, start: datetime, end: datetime, meeting_length: timedelta):
        potential_meetings = self.session.query(Schedule).filter(
            or_(
                and_(Schedule.StartTime <= start, Schedule.EndTime >= start),
                and_(Schedule.StartTime >= start, Schedule.StartTime <= end)
            ))

        result = []
        for meeting in potential_meetings.all():
            endtime = min(meeting.EndTime, end)
            starttime = max(meeting.StartTime, start)
            if endtime - starttime >= meeting_length:
                result.append({
                    'user': meeting.UID,
                    'start': starttime,
                    'end': endtime
                })

        return result
