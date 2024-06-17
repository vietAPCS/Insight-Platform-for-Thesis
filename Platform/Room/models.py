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
    prev_grade = models.IntegerField(null=False, blank=False)
    wanted_grade = models.IntegerField(null=False, blank=False)
    final_grade = models.IntegerField(null=True, blank=True)
    former_signature = models.TextField(max_length=255, blank=True, null=True)
    detail = models.ManyToManyField(User, related_name='room_detail', through='RoomDetails',  through_fields=('room_id', 'mentor_id'))

    def __str__(self):
        return str(self.community_id.name) + '-' + str(self.student_id.username) + '-' +str(self.id)
    
class RoomDetails(models.Model):
    room_id = models.ForeignKey(ExamRoom, on_delete=models.CASCADE)
    mentor_id = models.ForeignKey(User, on_delete=models.CASCADE)
    exam_cid = models.TextField(max_length=255, blank=True, null=True)
    answer_cid = models.TextField(max_length=255, blank=True, null=True)
    grade = models.IntegerField(default=0, blank=True, null=True)
    mentor_signature = models.TextField(max_length=255, blank=True, null=True)
    student_signature = models.TextField(max_length=255, blank=True, null=True)
    score_signature = models.TextField(max_length=255, blank=True, null=True)

    def __str__(self):
        return str(self.room_id)+ '-' + str(self.mentor_id.username)