from django.db import models
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

# Create your models here.
class ExamRoom(models.Model):
    id = models.AutoField(primary_key=True)
    mentor_id = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField(default=10, null=True, blank=True)
    mentor_hash = models.CharField(max_length=255, blank=True, null=False)
    student_hash = models.CharField(max_length=255, blank=True, null=False)

class StudentRoom(models.Model):
    room_id = models.ForeignKey(ExamRoom, on_delete=models.CASCADE)
    student_id = models.ForeignKey(User, on_delete=models.CASCADE)