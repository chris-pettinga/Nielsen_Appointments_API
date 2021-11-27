from rest_framework import serializers

from .models import Appointment


class AppointmentSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Appointment
		fields = ('date_time', 'status', 'price')

	def to_representation(self, instance):
		ret = super().to_representation(instance)
		ret['status'] = instance.get_status_display()
		return ret
