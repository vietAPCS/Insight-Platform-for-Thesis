from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from Community.models import Community
from Platform.utils import encrypt
# Create your models here.
class ExamRoom(models.Model):
    id = models.AutoField(primary_key=True)
    community_id = models.ForeignKey(Community, on_delete=models.CASCADE)
    student_id = models.ForeignKey(User, on_delete=models.CASCADE)
    final_grade = models.IntegerField(default=10, null=True, blank=True)
    former_signature = models.TextField(max_length=255, blank=True, null=False)
    detail = models.ManyToManyField(User, related_name='room_detail', through='RoomDetails')
    
class RoomDetails(models.Model):
    room_id = models.ForeignKey(ExamRoom, on_delete=models.CASCADE)
    mentor_id = models.ForeignKey(User, on_delete=models.CASCADE)
    exam_cid = models.TextField(max_length=255, blank=True, null=False)
    answer_cid = models.TextField(max_length=255, blank=True, null=False)
    grade = models.IntegerField(default=0, blank=True, null=False)
    student_signature = models.TextField(max_length=255, blank=True, null=False)
    mentor_signature = models.TextField(max_length=255, blank=True, null=False)
    def save(self, *args, **kwargs):
        self.exam_cid = encrypt(self.exam_cid)
        self.answer_cid = encrypt(self.answer_cid)
        super(RoomDetails, self).save(*args, **kwargs)