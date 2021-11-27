## NIELSEN APPOINTMENTS API

The Appointments API provides the user with an interface to view, change, and delete car service appointments

It's written in Python, using Django and specifically the django-rest-framework.

To run the web server:

1. Create a new Python virtual environment
2. Install the required dependencies `pip install -r requirements.txt`
3. Run migrations `python manage.py migrate`
4. Run the Django server `python manage.py runserver`
5. The server should now be running on localhost at port 8000 - '127.0.0.1:800'

The base API URL is '/api/applications/'

**All requests must have a trailing slash**

The endpoints exposed are:

1. `/api/applications/{id}/` - Returns a single Appointment object with the specified primary key. If it does not exist, a 404 is returned
2. `/api/applications/` - Returns a list of all Appointment objects in the database
3. ``



| Endpoint      | Request Type |  Result |
| ----------- | ----------- | ----------- |
| `api/applications/`      | GET       | Returns a list of all Appointment objects in the database |
| `/api/applications/{id}/` | GET        | Returns a single Appointment object with primary key {id}. If it does not exist, a 404 is returned |
| `/api/applications/{id}/` | DELETE        | Deletes the Appointment object with primary key {id}
| `/api/appointments/{id}/update_status/` | PUT        | Updates the status of the specified appointment with the status defined in the request body under the key 'status'. Available choices are [1,2,3] 
| `/api/appointments/get_appointments_between_dates/| GET        | Retrieves all the appointments between a specified date range, ordered by price (highest first). The start and end datetimes must be passed as query parameters: **start_date_time** and **end_date_time**. The datetime is in the format %YEAR-%MONTH-%DAYT%HOUR-%MINUTE-%SECOND. E.G. for the 13th December 2021 12PM, it would be 2021-12-13T12-00-00


