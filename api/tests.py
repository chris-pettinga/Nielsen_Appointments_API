import datetime

from django.test import TestCase
from rest_framework.test import APIClient

from .models import Appointment
from .serializers import AppointmentSerializer
from .utils import create_random_appointment


# Create your tests here.

class TestAppointmentAPI(TestCase):
	"""
	Testing the endpoints of the appointments API
	"""
	initial_random_appointments = 10

	def setUp(self):
		# Creating 10 random appointments
		random_appointments = []
		for i in range(self.initial_random_appointments):
			random_appointments.append(create_random_appointment())
		self.random_appointments = random_appointments

		self.client = APIClient()
		return super().setUp()

	def test_retrieve_all(self):
		# Testing if the /api/appointments endpoint will return all appointments in the DB
		r = self.client.get('/api/appointments/').json()

		self.assertEqual(len(r), self.initial_random_appointments)

		# Testing if all the appointments returned are what we expect, and not just duplicates of the same one for example
		for each in self.random_appointments:
			serialized_appointment = AppointmentSerializer(each)
			self.assertIn(serialized_appointment.data, r)

	def test_delete(self):
		# Testing that a DELETE request will delete the appropriate Appointment object

		self.assertEqual(Appointment.objects.count(), 10)
		r = self.client.delete('/api/appointments/1/')  # todo - dynamically generate the URL
		self.assertEqual(Appointment.objects.count(), 9)
		with self.assertRaises(Appointment.DoesNotExist):
			# Checking that the right object has been deleted
			Appointment.objects.get(pk=1)

	def test_update_status(self):
		# Testing the update_status endpoint
		new_appointment = Appointment.objects.create(
			status=1,
			date_time=datetime.datetime.now(),
			price=30
		)
		r = self.client.put(
			f'/api/appointments/{new_appointment.pk}/update_status/',
			{'status': 3}
		)
		new_appointment.refresh_from_db()
		self.assertEqual(new_appointment.status, 3)

	def test_retrieve_one(self):
		# Testing if we can retrieve just 1 particular Appointment object
		r = self.client.get('/api/appointments/1/').json()
		self.assertIsInstance(r, dict)

		# Testing if the Appointment returned by the API is the correct one
		serialized_db_object = AppointmentSerializer(Appointment.objects.get(pk=1)).data
		self.assertEqual(r, serialized_db_object)

	def test_create_random_appointments(self):
		# Testing that the create_random_appointments endpoint works
		self.assertEqual(Appointment.objects.count(), 10)
		r = self.client.post('/api/create_random_appointments/', {'number_new_appointments': 5})
		self.assertEqual(Appointment.objects.count(), 15)

class TestAppointmentsBetweenDates(TestCase):
	"""
	Testing the get_appointments_between_dates endpoint
	"""

	def test_appointments_between_dates_empty(self):
		# Testing that it returns an empty list if there are no appointment objects in the DB
		r = self.client.get(
			'/api/appointments/get_appointments_between_dates/?start_date_time=2020-12-13T12-00-00&end_date_time=2020-12-15T17-00-00'
		).json()
		self.assertEqual(r, [])

	def test_appointments_between_dates(self):
		# Testing that the right Appointment objects are returned when an appropriate date range is provided
		appointment_1 = Appointment.objects.create(
			date_time=datetime.datetime(
				year=2021,
				month=8,
				day=21,
				hour=12,
				minute=10,
				second=10,
				tzinfo=datetime.timezone.utc
			),
			price=500
		)
		appointment_1 = Appointment.objects.create(
			date_time=datetime.datetime(
				year=2021,
				month=8,
				day=22,
				hour=12,
				minute=10,
				second=10,
				tzinfo=datetime.timezone.utc
			),
			price=300
		)

		r = self.client.get(
			'/api/appointments/get_appointments_between_dates/?start_date_time=2021-08-19T12-00-00&end_date_time=2021-08-23T17-00-00'
		).json()
		self.assertEqual(len(r), 2)

		# Now checking if the results are ordered by price
		self.assertEqual(r[0]['price'], 500)
		self.assertEqual(r[1]['price'], 300)

		# Now if we make another request outside of the date range, we should expect an empty list
		r = self.client.get(
			'/api/appointments/get_appointments_between_dates/?start_date_time=2021-07-19T12-00-00&end_date_time=2021-07-23T17-00-00'
		).json()
		self.assertEqual(len(r), 0)
