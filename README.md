# Dosember Twitch Bot

This project is a Twitch bot designed to promote the event 'Dosember'. The bot periodically posts upcoming events from a Google Calendar into Twitch channels where it has been added as a moderator. It also responds to specific commands with predefined messages.

## Project Description

Dosember is an annual streaming event promoting DOS games. This bot helps in promoting the event by posting upcoming events and responding to user commands in Twitch channels.

## Setup Instructions

1. Clone the repository:
   ```
   git clone https://github.com/githubnext/workspace-blank.git
   cd workspace-blank
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Configure the bot:
   - Create a `.env` file in the root directory and add the following variables:
     ```
     TWITCH_BOT_USERNAME=<your-twitch-bot-username>
     TWITCH_OAUTH_TOKEN=<your-twitch-oauth-token>
     TWITCH_CHANNEL=<your-twitch-channel>
     GOOGLE_API_KEY=<your-google-api-key>
     GOOGLE_CALENDAR_ID=<your-google-calendar-id>
     ```

4. Run the bot:
   ```
   python bot.py
   ```

## Usage Instructions

The bot responds to the following commands in the Twitch chat:

- `!dosember`: Prints a message with a link to details about Dosember.
- `!schedule`: Displays the full schedule of events.
- `!remindme <event>`: Sets a reminder for a specific event.
- `!info`: Provides information about the event, participants, and other details.
- `!countdown`: Displays the time remaining until the next event.
- `!highlights`: Displays highlights or key moments from previous events.
- `!feedback`: Allows viewers to provide feedback or suggestions for the event.
- `/dosember`: Joins the channel and starts monitoring it.
