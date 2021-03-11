import asyncio
from model import ModelService


class BookingService:
    def __init__(self, modelsvc: ModelService):
        self.modelsvc = modelsvc

    def book_meeting(self, meeting_choice, current_user_id):
        other_user, start, end = meeting_choice['user'], meeting_choice['start'], meeting_choice['end']
        self.modelsvc.add_meeting(other_user, current_user_id)
        self.modelsvc.delete_schedule(other_user, start, end)

    # for cancel_meeting method: I think our 'Meetings' table should also have the Starttime and Endtime
    # Because if user1 cancels, then User2 must create a new 'Schedule' if
    # they want to meet at the same time as the cancelled meeting
    def cancel_meeting(self, meeting_choice):
        self.modelsvc.delete_meeting(meeting_choice.UID1, meeting_choice.UID2)

    def reschedule_meeting(self, new_meeting_choice, old_meeting_choice, current_user_id):
        other_user, start, end = new_meeting_choice['user'], new_meeting_choice['start'], new_meeting_choice['end']
        self.modelsvc.add_meeting(other_user, current_user_id)
        self.modelsvc.delete_meeting(old_meeting_choice.UID1, old_meeting_choice.UID2)