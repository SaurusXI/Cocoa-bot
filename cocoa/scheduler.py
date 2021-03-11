from datetime import datetime, timedelta
from model import ModelService
from notifier import NotifService
from discord import Client, TextChannel


class Scheduler:
    def __init__(self, modelsvc: ModelService, notifiersvc: NotifService, meeting_length: timedelta):
        self.meeting_length = meeting_length
        self.modelsvc = modelsvc
        self.notifiersvc = notifiersvc

    def schedule(self, uid: int, starttime: datetime, endtime: datetime, channel: TextChannel, client: Client):
        self.modelsvc.add_schedule(uid, starttime, endtime)

        potential_meetings = self.modelsvc.find_meetings(starttime, endtime, self.meeting_length)

        if potential_meetings:
            # Call notifier service and send notification of possible meetings
            self.notifiersvc.notify(potential_meetings, channel, client)
