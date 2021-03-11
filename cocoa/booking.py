import asyncio
from model import ModelService
from booking import BookingService

class BookService
    def __init__(self, modelsvc: ModelService, notifsvc: NotifService):
        self.modelsvc = modelsvc
        self.notifsvc = notifsvc

    def book_meetings(self, meeting_choices, current_user_id):
        for meeting in meeting_choices:
            other_user, start, end = meeting['user'], meeting['start'], meeting['end']
            modelsvc.add_meeting(other_user, current_user_id)
            modelsvc.delete_schedule(other_user, start, end)
        # To do: call notifier service and send notification that all meetings have been booked

    # for cancel_meeting method: I think our 'Meetings' table should also have the Starttime and Endtime
    # Because if user1 cancels, then User2 must create a new 'Schedule' if
    # they want to meet at the same time as the cancelled meeting
    def cancel_meeting(self, meeting_choice, current_user_id):
        modelsvc.delete_meeting(meeting_choice.UID1, meeting_choice.UID2)
        # To do: call notifier service and send notification that meeting has been cancelled
