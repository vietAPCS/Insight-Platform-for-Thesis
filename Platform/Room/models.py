from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from Community.models import Community

# Create your models here.
class ExamRoom(models.Model):
    id = models.AutoField(primary_key=True)
    community_id = models.ForeignKey(Community, on_delete=models.CASCADE)
    student_id = models.ForeignKey(User, on_delete=models.CASCADE)
    final_grade = models.IntegerField(default=10, null=True, blank=True)
    former_signature = models.TextField(max_length=255, blank=True, null=False)

class RoomDetails(models.Model):
    room_id = models.ForeignKey(ExamRoom, on_delete=models.CASCADE)
    mentor_id = models.ForeignKey(User, on_delete=models.CASCADE)
    exam_cid = models.TextField(max_length=255, blank=True, null=False)
    answer_cid = models.TextField(max_length=255, blank=True, null=False)
    grade = models.IntegerField(default=10, blank=True, null=False)
    student_signature = models.TextField(max_length=255, blank=True, null=False)
    mentor_signature = models.TextField(max_length=255, blank=True, null=False)