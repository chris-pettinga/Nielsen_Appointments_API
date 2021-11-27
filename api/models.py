from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.

class Appointment(models.Model):
	STATUS_CHOICES = (
		(1, 'Completed without issue'),
		(2, 'Completed with issues'),
		(3, 'Client did not show up'),
	)

	date_time = models.DateTimeField(verbose_name=_('Date and time of the appointment'))
	price = models.PositiveIntegerField(verbose_name=_('Price of the appointment'))
	status = models.PositiveSmallIntegerField(
		choices=STATUS_CHOICES,
		null=True,
		verbose_name=_('Status of the appointment')
	)
