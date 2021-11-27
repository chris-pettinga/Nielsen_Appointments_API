from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'appointments', views.AppointmentViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    #path('update_status/<pk>/<status>', views.UpdateAppointmentStatusView.as_view()),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]