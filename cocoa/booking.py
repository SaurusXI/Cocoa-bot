from cocoa.model import ModelService


class BookingService:
    def __init__(self, modelsvc: ModelService):
        self.modelsvc = modelsvc

    def book_meeting(self, meeting_choice, current_user_id):
        other_user, start, end = meeting_choice['user'], meeting_choice['start'], meeting_choice['end']
        self.modelsvc.add_meeting(other_user, current_user_id, start, end)
        self.modelsvc.delete_schedule(other_user, start, end)

    def cancel_meeting(self, meeting_choice):
        self.modelsvc.delete_meeting(meeting_choice.UID1, meeting_choice.UID2)

    def reschedule_meeting(self, new_meeting_choice, old_meeting_choice, current_user_id):
        self.cancel_meeting(meeting_choice=old_meeting_choice)
        self.book_meeting(meeting_choice=new_meeting_choice, current_user_id=current_user_id)

    # List all booked meetings
    def list_all_meetings(self, user_id):
        self.modelsvc.get_meetings(user_id)
