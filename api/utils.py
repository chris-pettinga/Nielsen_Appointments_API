import datetime
import random

from .models import Appointment


def create_random_appointment():
	"""
	Create a new Appointment object with semi-random (appropriate) values.
	"""

	status_choices = [each[0] for each in Appointment.STATUS_CHOICES]
	utc_now = datetime.datetime.now().replace(tzinfo=datetime.timezone.utc)

	return Appointment.objects.create(
		date_time=utc_now + datetime.timedelta(seconds=random.randint(0, 31540000)),
		price=random.randint(30, 1000),
		status=random.choice(status_choices)
	)
