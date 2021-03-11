from datetime import datetime, timedelta
from notifier import NotifierService
from model import ModelService
from discord import Client, TextChannel, User


class Scheduler:
    def __init__(self, modelsvc: ModelService, notifiersvc: NotifierService, meeting_length: timedelta):
        self.meeting_length = meeting_length
        self.modelsvc = modelsvc
        self.notifiersvc = notifiersvc

    def schedule(self, uid: int, starttime: datetime, endtime: datetime, channel: TextChannel, client: Client):
        self.modelsvc.add_schedule(uid, starttime, endtime)

        potential_meetings = self.modelsvc.find_meetings(starttime, endtime, self.meeting_length)

        if potential_meetings:
            # Call notifier service and send notification of possible meetings
            self.notifiersvc.notify_schedule(potential_meetings, channel, client)
    
    def cancel(self, uid: int, channel: TextChannel, client: Client):
        scheduled_meetings = self.modelsvc.get_meetings(uid=uid)
        self.notifiersvc.notify_cancel(scheduled_meetings, channel, client)

    def reschedule(self, uid: int, user: User, channel: TextChannel, client: Client):
        scheduled_meetings = self.modelsvc.get_meetings(uid=uid)
        self.notifiersvc.notify_reschedule(scheduled_meetings, user, channel, client)
