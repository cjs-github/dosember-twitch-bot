import os
import time
import logging
from datetime import datetime, timedelta
from twitchio.ext import commands
from googleapiclient.discovery import build

class DosemberBot(commands.Bot):

    def __init__(self):
        super().__init__(irc_token=os.environ['TWITCH_OAUTH_TOKEN'],
                         client_id=os.environ['TWITCH_CLIENT_ID'],
                         nick=os.environ['TWITCH_BOT_USERNAME'],
                         prefix='!',
                         initial_channels=[os.environ['TWITCH_CHANNEL']])
        self.google_api_key = os.environ['GOOGLE_API_KEY']
        self.google_calendar_id = os.environ['GOOGLE_CALENDAR_ID']
        self.calendar_service = build('calendar', 'v3', developerKey=self.google_api_key)
        self.logger = logging.getLogger('DosemberBot')
        self.logger.setLevel(logging.INFO)
        self.retry_attempts = 3

    async def event_ready(self):
        self.logger.info(f'Logged in as | {self.nick}')
        self.loop.create_task(self.periodic_event_check())

    async def event_message(self, message):
        await self.handle_commands(message)
        if message.content.strip().lower() == '/dosember':
            await self.join_channel_command(message.channel)

    async def join_channel(self, channel):
        if channel in self.connected_channels:
            self.logger.info(f'Already in channel: {channel}')
            return
        for attempt in range(self.retry_attempts):
            try:
                await self.join_channels([channel])
                self.logger.info(f'Joined channel: {channel}')
                return
            except Exception as e:
                self.logger.error(f'Failed to join channel {channel}: {e}')
                time.sleep(5)
        self.logger.error(f'Could not join channel {channel} after {self.retry_attempts} attempts')

    async def join_channel_command(self, channel):
        await self.join_channel(channel)
        await channel.send('Dosember bot has joined the channel!')

    async def periodic_event_check(self):
        while True:
            await self.post_upcoming_events()
            await asyncio.sleep(600)  # Check every 10 minutes

    async def post_upcoming_events(self):
        now = datetime.utcnow()
        time_min = now.isoformat() + 'Z'
        time_max = (now + timedelta(hours=48)).isoformat() + 'Z'

        events_result = self.calendar_service.events().list(
            calendarId=self.google_calendar_id,
            timeMin=time_min,
            timeMax=time_max,
            singleEvents=True,
            orderBy='startTime'
        ).execute()

        events = events_result.get('items', [])
        if not events:
            await self.connected_channels[0].send('No upcoming events in the next 48 hours.')
            return

        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            message = f"Upcoming event: {event['summary']} at {start}"
            await self.connected_channels[0].send(message)

    @commands.command(name='dosember')
    async def dosember(self, ctx):
        await ctx.send('Check out Dosember, an annual streaming event promoting DOS games! More details at: <link to details>')

    @commands.command(name='schedule')
    async def schedule(self, ctx):
        await ctx.send('Full schedule of events: <link to schedule>')

    @commands.command(name='remindme')
    async def remindme(self, ctx, *, event):
        await ctx.send(f'Reminder set for event: {event}')

    @commands.command(name='info')
    async def info(self, ctx):
        await ctx.send('Information about Dosember: <link to info>')

    @commands.command(name='countdown')
    async def countdown(self, ctx):
        now = datetime.utcnow()
        time_min = now.isoformat() + 'Z'
        time_max = (now + timedelta(hours=48)).isoformat() + 'Z'

        events_result = self.calendar_service.events().list(
            calendarId=self.google_calendar_id,
            timeMin=time_min,
            timeMax=time_max,
            singleEvents=True,
            orderBy='startTime'
        ).execute()

        events = events_result.get('items', [])
        if not events:
            await ctx.send('No upcoming events in the next 48 hours.')
            return

        next_event = events[0]
        start = datetime.fromisoformat(next_event['start'].get('dateTime', next_event['start'].get('date')))
        countdown = start - now
        await ctx.send(f'Time remaining until the next event: {countdown}')

    @commands.command(name='highlights')
    async def highlights(self, ctx):
        await ctx.send('Highlights or key moments from previous events: <link to highlights>')

    @commands.command(name='feedback')
    async def feedback(self, ctx):
        await ctx.send('Provide feedback or suggestions for the event: <link to feedback>')

if __name__ == '__main__':
    bot = DosemberBot()
    bot.run()
