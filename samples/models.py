from django.db import models
import uuid


class Sample(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    note = models.CharField(max_length=255, blank=True)
    amount = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    grant = models.UUIDField(primary_key=False, null=True)
    user = models.UUIDField(primary_key=False)
