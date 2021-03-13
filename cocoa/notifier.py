import asyncio
from discord import Client, TextChannel, User
from cocoa.model import ModelService
from cocoa.booking import BookingService


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
                self.bookingsvc.cancel_meeting(user_id)

    async def notify_reschedule(self, all_meetings, user: User, channel: TextChannel, client: Client):
        await channel.send(
            "Please type out your old meeting choice")
        try:
            old_meeting_choice = await client.wait_for('message', timeout=120)
        except asyncio.TimeoutError:
            return await channel.send('Sorry, you took too long.')
        
        # Ask for new meeting choice
        message_response = ''
        for meeting_info in all_meetings:
            user_id, start, end = meeting_info['user'], meeting_info['start'], meeting_info['end']
            message_response += 'Meeting with <@{}> from {} to {}'.format(user_id, start, end)

        # Print to the text channel
        await channel.send(
            "{}\n\nPlease choose a new meeting, by typing out a new User ID".format(message_response))
        try:
            new_meeting_choice = await client.wait_for('message', timeout=120)
        except asyncio.TimeoutError:
            return await channel.send('Sorry, you took too long to make a choice.')

        # Call the reschedule service
        for meeting_info in all_meetings:
            user_id = meeting_info['user']
            if user_id == new_meeting_choice:
                self.bookingsvc.reschedule_meeting(user_id, old_meeting_choice, user.id)

    async def notify_multiple_meetings(self, user: User, channel: TextChannel):
        user_meetings_notif = 'List of all the meetings you have booked :\n'
        all_user_meetings = self.bookingsvc.list_all_meetings(user.id)
        for meeting_info in all_user_meetings:
            user_id2 = meeting_info['user2']
            user_meetings_notif += 'Meeting with <@{}>'.format(user_id2)
        # Print to channel
        await channel.send(
            user_meetings_notif
        )