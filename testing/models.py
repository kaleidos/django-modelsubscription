from django.db import models

from modelsubscription.models import *

class TestModel(SubscriptableMixin, models.Model):
    pass
