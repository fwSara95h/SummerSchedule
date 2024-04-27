import json

# Load classes from JSON
with open('courses_info.json') as f:
    courses = json.load(f)
    classes = [{
        "name": f"{c} {i['name']}",
        **{("day" if k=="days" else k):v for k, v in i.items() if k != "name"},
        "class": c.replace(' ', '')
    } for c, i in courses.items()]

# Read the HTML template
# with open('template.html') as f: html_template = f.read()
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
  body { 
    font-family: Arial, sans-serif; 
    text-align: center; 
    margin: 0; 
    padding: 0; 
    justify-content: center; 
    align-items: center; 
    height: 100vh; 
    background-color: #f7f7f7; 
  }
  table { width: 100%; border-collapse: collapse; }
  th, td { border: 1px solid #ddd; text-align: center; }
  .time-header { background-color: #f2f2f2; }
  /*BACKGROUND COLORS*/ 
</style>
</head>
<body>

<h2>Weekly Schedule</h2>

<table>
  <tr class="time-header">
    <th>Time</th>
    <th>Sunday</th>
    <th>Monday</th>
    <th>Tuesday</th>
    <th>Wednesday</th>
    <th>Thursday</th>
    <th>Friday</th>
    <th>Saturday</th>
  </tr>
  <!--SCHEDULE_ROWS-->
</table>

</body>
</html>

"""

# Define time slots and days
time_slots = [f"{hour}:{'00' if minute == 0 else '30'}" 
              for hour in range(8, 17) for minute in [0, 30]]
days = ["Sunday", 
        "Monday", 
        "Tuesday", 
        "Wednesday", 
        "Thursday", 
        "Friday", 
        "Saturday"]

# Helper function to determine row span
def get_row_span(start_time, end_time):
    return int((end_time - start_time) * 2)

# Build the schedule rows
schedule_rows = ""
for time in time_slots:
    schedule_rows += f"<tr><td>{time}</td>"
    for day in days:
        cell_added = False
        for cls in classes:
            hr_half = '00' if cls['start_time'] % 1 == 0 else '30'
            start_str = f"{int(cls['start_time'])}:{hr_half}"
            if cls["day"] == day and start_str == time:
                rowspan = get_row_span(cls['start_time'], cls['end_time'])
                schedule_rows += (f"<td rowspan='{rowspan}' class='{cls['class']}'>"
                                  f"<b>{cls['name']}</b><br>"
                                  f"<i>{cls['location']}</i></td>")
                cell_added = True
                break
        if not cell_added:
            # Check if the time is during the duration of any class
            in_class = False
            for cls in classes:
                mid_time = float(time.split(':')[0]) 
                mid_time += (float(time.split(':')[1]) / 60)
                if (cls["day"] == day and
                    cls['start_time'] <= mid_time < cls['end_time']):
                    in_class = True
                    break
            if not in_class:
                schedule_rows += "<td></td>"
    schedule_rows += "</tr>\n"

# Integrate the schedule rows into the HTML template
final_html = html_template.replace(
    '<!--SCHEDULE_ROWS-->', schedule_rows
).replace('/*BACKGROUND COLORS*/', '\n  '.join([(
    f".{cls['class']}"
    f" {{ background-color: {cls['color']} }} "
    f"/* {cls['color_name']} */"
) for cls in classes]))

# Output the final HTML to a file
with open('index.html', 'w') as f:
    f.write(final_html)

print("Schedule generated successfully. Check index.html.")
