from ics import Calendar, Event
from datetime import datetime, timedelta, time
import pytz



# Define the course details in a dictionary format
courses_info = {
    "ELI 9200": {
        "name": "PLANNING & PROJECT MANAGEMENT",
        "section": "001 LEC 1175",
        "instructor": "Kevin Lawrence Mc Guire",
        "dates": "May 6 - July 22",
        "days": "Monday",
        "start_time": 13,  # 24-hour format
        "end_time": 16,
        "location": "AHB 1B02",
        "color": "#FFC0CB",  # Light Pink
    },
    "ELI 9300": {
        "name": "DESIGN DRIVEN INNOVATION",
        "section": "001 LEC 1106",
        "instructor": "Jacob Mackenzie Reeves",
        "dates": "May 10 - July 26",
        "days": "Friday",
        "start_time": 12.5,
        "end_time": 15.5,
        "location": "AHB 2B04",
        "color": "#ADD8E6",  # Light Blue
    },
    "ELI 9400": {
        "name": "ENGINEERING LEADERSHIP",
        "section": "001 LEC 1177",
        "instructor": "Minha R. Ha",
        "dates": "May 7 - July 23",
        "days": "Tuesday",
        "start_time": 8.5,
        "end_time": 11.5,
        "location": "TC 203",
        "color": "#90EE90",  # Light Green
    },
    "ELI 9600": {
        "name": "ENGINEERING COMMUNICATIONS",
        "section": "001 LEC 1178",
        "instructor": "Natalie Mathieson",
        "dates": "May 7 - July 25",
        "days": "Tuesday",
        "start_time": 12.5,
        "end_time": 15.5,
        "location": "AHB 2B04",
        "color": "#FFFFE0",  # Light Yellow
    }
}

# Create a Calendar
calendar = Calendar()

# Define the timezone
timezone = 'America/Toronto'
local_tz = pytz.timezone(timezone)

# Helper function to create datetime objects
def create_event_date(date_str, hour, tz_info):
    # Create a date object for the event
    date_obj = datetime.strptime(date_str, "%Y %B %d")
    # Return the datetime combined with the hour, set to the correct timezone
    return tz_info.localize(datetime.combine(date_obj, time(int(hour), int((hour % 1) * 60))))

# Iterate over the courses to create events
for course_code, course in courses_info.items():
    # Parse the start and end dates
    start_date_str = f"2024 {course['dates'].split(' - ')[0]}"
    end_date_str = f"2024 {course['dates'].split(' - ')[1]}"
    
    # Calculate the event start and end times
    start_datetime = create_event_date(start_date_str, course['start_time'], local_tz)
    end_datetime = create_event_date(start_date_str, course['end_time'], local_tz)

    # Create events for each week until the end date
    current_date = start_datetime
    end_date = create_event_date(end_date_str, course['end_time'], local_tz)
    while current_date <= end_date:
        # Create an event
        event = Event()
        event.name = f"{course_code} {course['name']}"
        event.begin = current_date
        event.end = current_date + timedelta(hours=course['end_time'] - course['start_time'])
        event.location = course['location']
        event.description = f"Instructor: {course['instructor']} \nSection: {course['section']}"
        # Add the event to the calendar
        calendar.events.add(event)
        # Increment the current date by a week
        current_date += timedelta(days=7)

# Save the calendar to an ICS file
ics_file_path = 'university_schedule.ics'
with open(ics_file_path, 'w') as my_file:
    my_file.writelines(str(calendar))

print("saved to", ics_file_path)

