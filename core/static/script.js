const toggle = document.getElementById('toggle');
const statusText = document.getElementById('status');
const eventsTable = document.getElementById('eventsTable');
const eventsBody = document.getElementById('eventsBody');
const startTimeInput = document.getElementById('startTime');
const endTimeInput = document.getElementById('endTime');
const errorMessage = document.getElementById('errorMessage');
const setTimes = document.getElementById('setTimes');
const displayStartTime = document.getElementById('displayStartTime');
const displayEndTime = document.getElementById('displayEndTime');

// Function to set toggle button state based on localStorage
function setToggleButtonState() {
  const state = localStorage.getItem('alarmState');
  const startTime = localStorage.getItem('startTime');
  const endTime = localStorage.getItem('endTime');

  if (state === 'on' && startTime && endTime) {
    toggle.checked = true;
    statusText.textContent = 'on';
    displayStartTime.textContent = startTime;
    displayEndTime.textContent = endTime;
    setTimes.style.display = 'block';
  } else {
    toggle.checked = false;
    statusText.textContent = 'off';
    setTimes.style.display = 'none';
  }
}

// Function to round time to the nearest 10 minutes
function roundToNearest10Minutes(time) {
  const [hours, minutes] = time.split(':').map(Number);
  const roundedMinutes = Math.round(minutes / 10) * 10;
  const adjustedHours = (roundedMinutes === 60) ? (hours + 1) % 24 : hours;
  const adjustedMinutes = (roundedMinutes === 60) ? 0 : roundedMinutes;
  return `${String(adjustedHours).padStart(2, '0')}:${String(adjustedMinutes).padStart(2, '0')}`;
}

// Event listener to round start time to nearest 10 minutes
startTimeInput.addEventListener('blur', function() {
  if (startTimeInput.value) {
    startTimeInput.value = roundToNearest10Minutes(startTimeInput.value);
  }
});

// Event listener to round end time to nearest 10 minutes
endTimeInput.addEventListener('blur', function() {
  if (endTimeInput.value) {
    endTimeInput.value = roundToNearest10Minutes(endTimeInput.value);
  }
});

// Event listener for toggle button change
// Event listener for toggle button change
toggle.addEventListener('change', function() {
  const startTime = startTimeInput.value;
  const endTime = endTimeInput.value;

  if (this.checked && (!startTime || !endTime)) {
    errorMessage.style.display = 'block';
    toggle.checked = false;
    return;
  }

  errorMessage.style.display = 'none';
  const alarmState = this.checked ? 'on' : 'off';

  updateAlarmState(alarmState, startTime, endTime);

  if (alarmState === 'on') {
    localStorage.setItem('startTime', startTime);
    localStorage.setItem('endTime', endTime);
    displayStartTime.textContent = startTime;
    displayEndTime.textContent = endTime;
    setTimes.style.display = 'block';
  } else {
    localStorage.removeItem('startTime');
    localStorage.removeItem('endTime');
    setTimes.style.display = 'none';
  }
});


// Function to update alarm state via AJAX
function updateAlarmState(alarmState, startTime, endTime) {
  const isAlarmOn = alarmState === 'on'; // Convert 'on'/'off' to boolean

  fetch('/set_alarm', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ alarm_state: isAlarmOn, start_time: startTime, end_time: endTime }),
  })
    .then(response => response.json())
    .then(data => {
      console.log('Alarm state updated successfully:', data.message);
      localStorage.setItem('alarmState', isAlarmOn); // Update localStorage with boolean
      statusText.textContent = isAlarmOn ? 'on' : 'off'; // Update status text
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

// Function to fetch alarm state from backend
function fetchAlarmStateFromBackend() {
    fetch('/alarm_state')
        .then(response => response.json())
        .then(data => {
            // Use fetched data to update UI elements
            console.log('Fetched alarm state:', data);

            // Update localStorage with fetched alarm state
            localStorage.setItem('alarmState', data.alarm_state);
            localStorage.setItem('startTime', data.startTime);
            localStorage.setItem('endTime', data.endTime);

            // Update UI elements related to alarm state
            updateAlarmStateUI(data.alarm_state, data.startTime, data.endTime);
        })
        .catch(error => console.error('Error fetching alarm state:', error));
}

// Function to update UI elements based on alarm state
function updateAlarmStateUI(alarmState, startTime, endTime) {
    const toggle = document.getElementById('toggle');
    const statusText = document.getElementById('status');
    const displayStartTime = document.getElementById('displayStartTime');
    const displayEndTime = document.getElementById('displayEndTime');
    const setTimes = document.getElementById('setTimes');

    if (alarmState) {
        toggle.checked = true;
        statusText.textContent = 'on';
        displayStartTime.textContent = startTime;
        displayEndTime.textContent = endTime;
        setTimes.style.display = 'block';
    } else {
        toggle.checked = false;
        statusText.textContent = 'off';
        setTimes.style.display = 'none';
    }
}

// Initialize toggle button state and events on page load
setToggleButtonState();
const cachedEvents = getEventsFromLocalStorage();
if (cachedEvents.length > 0) {
  displayEvents(cachedEvents);
}

// Fetch events every 5 seconds
setInterval(fetchEvents, 5000);
fetchAlarmStateFromBackend();