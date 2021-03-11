import asyncio
from discord import Client, TextChannel
from model import ModelService
from booking import BookingService


# main class for notification service
class NotifierService:
    def __init__(self, bookingsvc: BookingService, current_user_id: int):
        self.bookingsvc = bookingsvc
        self.current_user_id = current_user_id

    # Notify method
    async def notify_schedule(self, all_meetings, channel: TextChannel, client: Client):
        message_response = ''
        for meeting_info in all_meetings:
            user_id, start, end = meeting_info['user'], meeting_info['start'], meeting_info['end']
            message_response += 'Meeting with <@{}> from {} to {}'.format(user_id, start, end)

        # Print to the text channel
        await channel.send(
            "{}\n\nPlease choose which meeting you want to book, by typing out the User ID".format(message_response))
        try:
            meeting_choice = await client.wait_for('message', timeout=120)
        except asyncio.TimeoutError:
            return await channel.send('Sorry, you took too long to make a choice.')

        for meeting_info in all_meetings:
            user_id = meeting_info['user']
            if user_id == meeting_choice:
                self.bookingsvc.book_meeting(meeting_info, self.current_user_id)

    async def notify_cancel(self, all_meetings, channel: TextChannel, client: Client):
        message_response = ''
        for meeting_info in all_meetings:
            user_id, start, end = meeting_info['user'], meeting_info['start'], meeting_info['end']
            message_response += 'Meeting with <@{}> from {} to {}'.format(user_id, start, end)

        # Print to the text channel
        await channel.send(
            "{}\n\nPlease choose which meeting you want to cancel, by typing out the User ID".format(message_response))
        try:
            meeting_choice = await client.wait_for('message', timeout=120)
        except asyncio.TimeoutError:
            return await channel.send('Sorry, you took too long to make a choice.')

        for meeting_info in all_meetings:
            user_id = meeting_info['user']
            if user_id == meeting_choice:
                self.bookingsvc.cancel_meeting(meeting_info)


