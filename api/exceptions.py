from rest_framework.exceptions import APIException

class AppointmentAPIBadRequestException(APIException):
	status_code = 400
