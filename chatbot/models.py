import time

from django.db import models
from django.conf import settings


# Create your models here.

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class Thread(BaseModel):
    thread_id = models.CharField(max_length=100, unique=True)
    session_id = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.thread_id

    class Meta:
        db_table = "thread"


class Message(BaseModel):
    thread = models.ForeignKey(Thread, on_delete=models.SET_NULL, null=True, blank=True)
    question = models.TextField(null=True, blank=True)
    answer = models.TextField(null=True, blank=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = "message"