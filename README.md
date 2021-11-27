## NIELSEN APPOINTMENTS API

The Appointments API provides the user with an interface to view, change, and delete car service appointments

It's written in Python, using Django and specifically the django-rest-framework.

To run the web server:

1. Create a new Python virtual environment
2. Install the required dependencies `pip install -r requirements.txt`
3. Run migrations `python manage.py migrate`
4. Run the Django server `python manage.py runserver`
5. The server should now be running on localhost at port 8000 - '127.0.0.1:8000'

The base API URL is '/api/applications/'

**All requests must have a trailing slash**

A function for generating random appointments can be found in the `api/utils.py` file. By making a POST request to `/api/appointments/create_random_appointments/` with key `number_new_appointments` in the request body, the specified number of random appointments will be created in the database. 

The endpoints exposed are:

| Endpoint      | Request Type |  Result |
| ----------- | ----------- | ----------- |
| `api/applications/`      | GET       | Returns a list of all Appointment objects in the database |
| `/api/applications/{id}/` | GET        | Returns a single Appointment object with primary key {id}. If it does not exist, a 404 is returned |
| `/api/applications/{id}/` | DELETE        | Deletes the Appointment object with primary key {id}
| `/api/appointments/{id}/update_status/` | PUT        | Updates the status of the specified appointment with the status defined in the request body under the key 'status'. Available choices are [1,2,3] 
| `/api/appointments/get_appointments_between_dates/`| GET        | Retrieves all the appointments between a specified date range, ordered by price (highest first). The start and end datetimes must be passed as query parameters: **start_date_time** and **end_date_time**. The datetime is in the format %YEAR-%MONTH-%DAYT%HOUR-%MINUTE-%SECOND. E.G. for the 13th December 2021 12PM, it would be 2021-12-13T12-00-00


I have also included an example config.yml file that would be used in conjunction with CircleCI/Docker to create a CI pipeline

### Things that could be improved
1. The entire package could be wrapped in a docker image, making deployment a lot easier. This would be useful for you as the interviewer but also in production alongside the CI automatic testing suite
2. Sqlite is not an appropriate DB choice for a production application, in reality I would use Postgres however for the sake of making deployment easier, I went with Sqlite
3. Better documentation explaining how to use the API (e.g. example requests, example repsonses, data-types of all possible responses...etc.) would be very useful
4. User authentication and rate limiting to ensure that only authenticated and responsible users could access the API. This would perhaps be done in the form of an personal API key given to clients. 
5. Similar to above, appointments could be linked to the users in the database, further improving data-access controls by only allowing clients to see the Appointments they have a relationship with
6. I'm not too happy about the 'status' field of the Appointment model, it seems strange that a new record is created with a null value and is then only given one when the appointment has happened. Data in one table should all pertain to the state of that object at a single point in time, perhaps a one-to-many child table would be better to deal with appointment results and follow-ups