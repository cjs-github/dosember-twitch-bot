const tmi = require('tmi.js');
const { google } = require('googleapis');
const config = require('./config');
const commands = require('./commands');
const utils = require('./utils');

// Initialize Twitch bot
const client = new tmi.Client({
  options: { debug: true },
  identity: {
    username: config.TWITCH_BOT_USERNAME,
    password: config.TWITCH_OAUTH_TOKEN
  },
  channels: [config.TWITCH_CHANNEL]
});

client.connect();

// Initialize Google Calendar API
const calendar = google.calendar({ version: 'v3', auth: config.GOOGLE_API_KEY });

// Function to post upcoming events
async function postUpcomingEvents() {
  const now = new Date();
  const timeMin = now.toISOString();
  const timeMax = new Date(now.getTime() + 48 * 60 * 60 * 1000).toISOString();

  const res = await calendar.events.list({
    calendarId: config.GOOGLE_CALENDAR_ID,
    timeMin: timeMin,
    timeMax: timeMax,
    singleEvents: true,
    orderBy: 'startTime'
  });

  const events = res.data.items;
  if (events.length) {
    events.forEach(event => {
      const start = event.start.dateTime || event.start.date;
      client.say(config.TWITCH_CHANNEL, `Upcoming event: ${event.summary} at ${start}`);
    });
  } else {
    client.say(config.TWITCH_CHANNEL, 'No upcoming events in the next 48 hours.');
  }
}

// Periodically post upcoming events
setInterval(postUpcomingEvents, 60 * 60 * 1000); // Every hour

// Respond to specific commands
client.on('message', (channel, tags, message, self) => {
  if (self) return;

  const command = message.trim().toLowerCase();

  if (commands[command]) {
    client.say(channel, commands[command]);
  } else if (command.startsWith('!remindme')) {
    const event = command.split(' ')[1];
    // Handle remindme command
    client.say(channel, `Reminder set for event: ${event}`);
  } else if (command === '!schedule') {
    // Handle schedule command
    client.say(channel, 'Full schedule of events: <link to schedule>');
  } else if (command === '!info') {
    // Handle info command
    client.say(channel, 'Information about Dosember: <link to info>');
  }
});

// Function to join a channel when a user types /dosember
client.on('message', (channel, tags, message, self) => {
  if (self) return;

  if (message.trim().toLowerCase() === '/dosember') {
    client.join(channel).then(() => {
      client.say(channel, 'Dosember bot has joined the channel!');
    }).catch(err => {
      console.error(err);
    });
  }
});

// Function to check for an existing bot to avoid duplication
client.on('join', (channel, username, self) => {
  if (self) {
    client.say(channel, 'Dosember bot is already in the channel.');
  }
});
