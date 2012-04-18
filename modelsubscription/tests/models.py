from django.db import models
from ..models import *

class TestModel(SubscriptableMixin, models.Model):
    pass
