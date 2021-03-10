from datetime import datetime, timedelta
from model import ModelService

class Scheudler:
    def __init__(self, modelsvc: ModelService, meeting_length: timedelta):
        self.meeting_length = meeting_length
        self.modelsvc = modelsvc

    def schedule(self, uid: int, starttime: datetime, endtime: datetime):
        self.modelsvc.add_schedule(uid, starttime, endtime)

        potential_meetings = self.modelsvc.find_meetings(starttime, endtime, self.meeting_length)

        # To do - call notifier service and send notification of possible meetings
        # self.notifiersvc.notify(potential_meetings, ...)
