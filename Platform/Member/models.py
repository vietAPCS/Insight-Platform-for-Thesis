from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from Community.models import Community
from django.db.models.signals import post_save
from django.dispatch import receiver
from PIL import Image

# Create your models here.
class MyUser(models.Model):
    id = models.AutoField(primary_key = True)
    userid = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True, related_name="myuser")
    metamaskID = models.CharField(max_length=255, blank=True, null=True)
    avatar = models.ImageField(default='default.png', upload_to='profile_images')
    def __str__(self):
        return str(self.userid)
    def save(self, *args, **kwargs):
        super().save()
        img = Image.open(self.avatar.path)
        if img.height > 200 or img.width > 200:
            new_img = (200, 200)
            img.thumbnail(new_img)
            img.save(self.avatar.path)
    
class UserHistory(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    update_date = models.DateField(auto_now_add=True)
    community_id = models.ForeignKey(Community, on_delete=models.CASCADE)
    content = models.CharField(max_length=255)
    def save(self, *args, **kwargs):
        # Get the day, month, and year from the created_date
        day = str(self.update_date.day).zfill(2)
        month = str(self.update_date.month).zfill(2)
        year = str(self.update_date.year % 100).zfill(2)

        # Concatenate community_id and formatted created_date to generate commu_history_id
        self.id = f"{self.user_id}-{self.community_id}-{day}{month}{year}"

        super().save(*args, **kwargs)


class UserCommunity(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_community")
    community_id = models.ForeignKey(Community, on_delete=models.CASCADE)
    score = models.IntegerField(default=10, null=True, blank=True)
    joined_date = models.DateField(auto_now_add=True)
    is_mentor = models.BooleanField(default=False, null=False, blank=True)
    def __str__(self):
        return str(self.user_id) + ' - ' + str(self.community_id)

class RequestMentor(models.Model):
    id = models.AutoField(primary_key=True)
    UserCommunityId = models.ForeignKey(UserCommunity, on_delete=models.CASCADE, related_name="member_in_community")
    mentorId =  models.ForeignKey(UserCommunity, on_delete=models.CASCADE, related_name="requesting_mentors")
    upadate_date = models.DateField(auto_now_add=True)
    status = models.IntegerField(default= 0, blank=True, null=True) #1 == accepted, 2 == reject, 0 == waiting