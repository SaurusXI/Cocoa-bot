import asyncio
from datetime import datetime, timedelta
from cocoa.notifier import NotifierService
from cocoa.model import ModelService
from discord import Client, TextChannel, User


async def get_time(message: str, channel: TextChannel, client: Client):
    await channel.send(message)
    try:
        response = await client.wait_for('message', timeout=300)
    except asyncio.TimeoutError:
        return await channel.send('Sorry, you took too long to decide !')
    return response


async def get_start_end_time(channel: TextChannel, client: Client):
    start = get_time("Please type the start time of the meeting in the format %m/%d/%Y, %H:%M:%S", channel, client)
    end = get_time("Please type the end time of the meeting in the format %m/%d/%Y, %H:%M:%S", channel, client)
    start = datetime.strptime(start, "%m/%d/%Y, %H:%M:%S")
    end = datetime.strptime(end, "%m/%d/%Y, %H:%M:%S")

    return start, end


class Scheduler:
    def __init__(self, modelsvc: ModelService, notifiersvc: NotifierService, meeting_length: timedelta):
        self.meeting_length = meeting_length
        self.modelsvc = modelsvc
        self.notifiersvc = notifiersvc

    def schedule(self, uid: int, channel: TextChannel, client: Client):
        start_time, end_time = get_start_end_time(channel, client)
        self.modelsvc.add_schedule(uid, start_time, end_time)
        potential_meetings = self.modelsvc.find_meetings(start_time, end_time, self.meeting_length)
        potential_meetings = potential_meetings[0:5]

        if potential_meetings:
            # Call notifier service and send notification of possible meetings
            self.notifiersvc.notify_schedule(potential_meetings, channel, client, current_user_id=uid)

    def cancel(self, uid: int, channel: TextChannel, client: Client):
        scheduled_meetings = self.modelsvc.get_meetings(uid=uid)
        self.notifiersvc.notify_cancel(scheduled_meetings, channel, client)

    def reschedule(self, uid: int, user: User, channel: TextChannel, client: Client):
        scheduled_meetings = self.modelsvc.get_meetings(uid=uid)
        self.notifiersvc.notify_reschedule(scheduled_meetings, user, channel, client)

    def list_booked_meetings(self, user: User, channel: TextChannel):
        self.notifiersvc.notify_multiple_meetings(user, channel)

