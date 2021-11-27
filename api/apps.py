from django.apps import AppConfig
import threading
import random

class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'

    def ready(self):
        x = threading.Thread(target=random_appointment_scheduler, daemon=True)
        #x.start()


def random_appointment_scheduler():
    """
    Will create new appointments in the database at random intervals.

    TODO - really should've used celery for this
    """
    from .utils import create_random_appointment

    while True:
        random_chance = random.randint(1, 500000000)
        if random_chance == 1:
            create_random_appointment()
            print('Random appointment created')