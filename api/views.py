from datetime import datetime, timezone

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import status as rs_status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .exceptions import AppointmentAPIBadRequestException
from .models import Appointment
from .serializers import AppointmentSerializer


# Create your views here.

class AppointmentViewSet(viewsets.ModelViewSet):
	"""
	View dealing with all API requests.

	Most of the basic stuff (get all, delete one...etc) are handled by the django-rest-framework (DRF) library. Additional
	endpoints (like update_status) are manually created here.

	todo - As the API is quite simple, this is fine as 1 single class. However as functionality grows, it would be wise to
	split the API into different views, each dealing with a different type/function of request
	"""
	queryset = Appointment.objects.all().order_by('date_time')
	serializer_class = AppointmentSerializer

	@action(methods=['put'], detail=True)
	def update_status(self, request, pk):
		"""PUT - Update status of a particular Appointment object"""
		new_status = request.data.get('status', None)
		if not new_status:
			status_choices = ''.join([f'{each[0]} - {each[1]}. ' for each in Appointment.STATUS_CHOICES])
			raise AppointmentAPIBadRequestException(
				detail=f"Missing 'status' parameter in request body. The available choices are {status_choices}"
			)
		appointment_object = get_object_or_404(Appointment, pk=pk)
		appointment_serializer = AppointmentSerializer(appointment_object, data=request.data, partial=True)
		if appointment_serializer.is_valid():
			appointment_serializer.save()
			return JsonResponse(data=appointment_serializer.data, status=rs_status.HTTP_201_CREATED)
		return JsonResponse(data=appointment_serializer.errors, status=rs_status.HTTP_400_BAD_REQUEST)

	@action(methods=['get'], list=True, detail=False)
	def get_appointments_between_dates(self, request):
		"""
		GET - Return a list of appointments between 2 particular datetimes defined in the URL query parameters and
		return them sorted by price
		"""
		# we presume all the datetimes are in the same timezone (UTC), this can be improved upon in the future if the
		# company starts dealing with appointments in different timezones

		start_date_time = request.GET.get('start_date_time')
		end_date_time = request.GET.get('end_date_time')

		try:
			start_date = datetime.strptime(
				start_date_time,
				'%Y-%m-%dT%H-%M-%S'
			).replace(tzinfo=timezone.utc)
			end_date = datetime.strptime(
				end_date_time,
				'%Y-%m-%dT%H-%M-%S'
			).replace(tzinfo=timezone.utc)
		except (ValueError, TypeError) as e:
			# ValueError for if the dates are incorrectly formatted
			# TypeError for if they have not been provided at all in the URL parameters
			raise AppointmentAPIBadRequestException(
				detail='Please provide the start and end date/time in the correct format during which you would like to retrieve scheduled appointments. This can be done using the query parameters \'start_date_time\' and \'end_date_time\' in the format YEAR-MONTH-DAYTHOUR-MINUTE-SECOND e.g. to find all scheduled appointments between 12PM on the 13th December 2021 and 5pm on the 15th December 2021,the URL would look like /api/appointments/get_appointments_between_dates?start_date_time=2021-12-13T12-00-00&end_date_time=2021-12-15T17-00-00'
			)

		if start_date >= end_date:
			raise AppointmentAPIBadRequestException(
				detail='The end date/time cannot be before the start date/time'
			)

		relevant_appointments = Appointment.objects.filter(
			date_time__gte=start_date,
			date_time__lte=end_date
		).order_by('-price')

		serialized_data = AppointmentSerializer(relevant_appointments, many=True)
		return Response(data=serialized_data.data, status=rs_status.HTTP_200_OK)
