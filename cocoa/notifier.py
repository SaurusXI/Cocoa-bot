import asyncio
from discord import Client, TextChannel
from model import ModelService
from booking import BookingService

# main class for notification service
class NotifService:
    def __init__(self, modelsvc: ModelService, bookingsvc: BookingService):
        self.modelsvc = modelsvc
        self.bookingsvc = bookingsvc

    # Notify method
    async def notify(self, all_meetings, channel: TextChannel, client: Client):
        message_response = ''
        for meeting_info in all_meetings:
            user_id,start,end = meeting_info['user'],meeting_info['start'],meeting_info['end']
            message_response += 'Meeting with <@{}> from {} to {}'.format(user_id,start,end)

        # Print to the text channel
        await channel.send("{}\n\nPlease choose which meeting you want to book, by typing out the User ID".format(message_response))
        try:
            meeting_choice = await client.wait_for('message', timeout=120)
        except asyncio.TimeoutError:
            return await channel.send('Sorry, you took too long to make a choice.')

        # TODO: Call the booking service to book a meeting based on the user's choice/re-schedule the meeting/cancel the meeting
        # self.bookingsvc.book_meeting(all_meetings,meeting_choice, ...)
