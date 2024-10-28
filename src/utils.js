const moment = require('moment');

// Utility functions for date and time calculations
function getTimeDifference(startTime, endTime) {
  const start = moment(startTime);
  const end = moment(endTime);
  return end.diff(start, 'minutes');
}

function isEventWithinNext48Hours(eventTime) {
  const now = moment();
  const event = moment(eventTime);
  return event.isBetween(now, now.add(48, 'hours'));
}

// Utility functions for formatting messages
function formatEventMessage(event) {
  const start = moment(event.start.dateTime || event.start.date).format('MMMM Do YYYY, h:mm:ss a');
  return `Upcoming event: ${event.summary} at ${start}`;
}

module.exports = {
  getTimeDifference,
  isEventWithinNext48Hours,
  formatEventMessage
};
