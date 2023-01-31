from datetime import datetime
from django.utils import timezone

class timezone:
    '''Cette classe a été créée pour le besoin de test. A remplacer directement par timezone.now() au besoin'''
    def now():
        return timezone.now()
        # return datetime(2023, 1, 26, 15, 8 )