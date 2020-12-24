import uuid

from django.db import models
from django.contrib.auth import get_user_model


class Group(models.Model):

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    title = models.CharField(max_length=250, null=False)
    admin = models.ForeignKey(get_user_model(), related_name='admin_teams', on_delete=models.CASCADE, null=False)
    members = models.ManyToManyField(get_user_model(), related_name='teams', null=True)
