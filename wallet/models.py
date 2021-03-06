import uuid

from django.db import models
from django.contrib.auth import get_user_model


class Wallet(models.Model):

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    amount = models.FloatField(default=0.0)
