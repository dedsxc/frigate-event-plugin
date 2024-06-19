const toggle = document.getElementById('toggle');
const statusText = document.getElementById('status');
const eventsTable = document.getElementById('eventsTable');
const eventsBody = document.getElementById('eventsBody');

// Function to set toggle button state based on localStorage
function setToggleButtonState() {
  const state = localStorage.getItem('alarmState');
  if (state === 'on') {
    toggle.checked = true;
    statusText.textContent = 'on';
  } else {
    toggle.checked = false;
    statusText.textContent = 'off';
  }
}

// Event listener for toggle button change
toggle.addEventListener('change', function() {
  const alarmState = this.checked ? 'on' : 'off';
  updateAlarmState(alarmState);
});

// Function to update alarm state via AJAX
function updateAlarmState(alarmState) {
  fetch('/set_alarm', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ alarm_state: alarmState }),
  })
    .then(response => response.json())
    .then(data => {
      console.log('Alarm state updated successfully:', data.message);
      localStorage.setItem('alarmState', alarmState); // Update localStorage
      statusText.textContent = alarmState;
    })
    .catch(error => console.error('Error updating alarm state:', error));
}

// Function to save events to localStorage
function saveEventsToLocalStorage(events) {
  localStorage.setItem('events', JSON.stringify(events));
}

// Function to get events from localStorage
function getEventsFromLocalStorage() {
  const events = localStorage.getItem('events');
  return events ? JSON.parse(events) : [];
}

// Function to format Unix timestamp to human-readable date and time
function formatUnixTimestamp(timestamp) {
  const date = new Date(timestamp * 1000); // JavaScript Date constructor expects milliseconds, so multiply by 1000
  return date.toLocaleString(); // Convert to local date and time string
}

function displayEvents(events) {
  eventsBody.innerHTML = ''; // Clear the table body before adding new events
  events.forEach(event => {
    const row = document.createElement('tr');

    // ID column
    const idCell = document.createElement('td');
    idCell.textContent = event.before.id;
    row.appendChild(idCell);

    // Data columns
    const fields = ['label', 'camera', 'score', 'false_positive', 'start_time', 'stationary'];
    fields.forEach(field => {
      const cell = document.createElement('td');
      if (field === 'start_time') {
        cell.textContent = formatUnixTimestamp(event.before[field]);
      } else {
        cell.textContent = event.before[field];
      }
      row.appendChild(cell);
    });

    eventsBody.appendChild(row);
  });
}

function fetchEvents() {
  fetch('/events')
    .then(response => response.json())
    .then(events => {
      saveEventsToLocalStorage(events); // Save events to localStorage
      displayEvents(events); // Display events in the UI
    })
    .catch(error => console.error('Error fetching events:', error));
}

// Initialize toggle button state and events on page load
setToggleButtonState();
const cachedEvents = getEventsFromLocalStorage();
if (cachedEvents.length > 0) {
  displayEvents(cachedEvents);
}

// Fetch events every 5 seconds
setInterval(fetchEvents, 5000);
