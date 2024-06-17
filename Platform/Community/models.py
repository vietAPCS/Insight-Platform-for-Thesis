from ast import Num
from django.db import models
from django.contrib.auth.models import User
# from Member.models import User
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from Platform.utils import encrypt
def validate_no_negative(value):
    if value < 0:
        raise ValidationError(
            _('%(value)s is not a positive value'),
            params={'value': value},
        )
    
# Create your models here.
class Community(models.Model):
    # khóa đại diện , khóa chính
    id = models.AutoField(primary_key=True) 
    name = models.CharField(max_length=255, blank=True, null=True)
    created_date = models.DateField(auto_now_add=True, blank=True, null=True)
    created_user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=255, blank=True, null=True)
    upload_permission = models.IntegerField(default=1, blank=True, null=True)
    mentor_threshold = models.IntegerField(default=0, validators=[validate_no_negative])
    entrance_test_enable = models.BooleanField(default=0)
    # Member = models.ManyToManyField(User,related_name='groups_joined',through='CommunityMember')

    def __str__(self):
        return str(self.name) + '-' + str(self.created_user)
    
    def get_absolute_url(selft):
        return reverse('home')

class CommunityHistory(models.Model):
    commu_history_id = models.AutoField(primary_key=True)
    community_id = models.ForeignKey(Community, on_delete=models.CASCADE, null = False)
    updated_date = models.DateField(auto_now_add=True, null=False)
    updated_content = models.CharField(max_length=255, blank=True, null=False)
    updated_user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    def save(self, *args, **kwargs):
        # Get the day, month, and year from the created_date
        day = str(self.created_date.day).zfill(2)
        month = str(self.created_date.month).zfill(2)
        year = str(self.created_date.year % 100).zfill(2)

        # Concatenate community_id and formatted created_date to generate commu_history_id
        self.commu_history_id = f"{self.community_id}-{day}{month}{year}"

        super().save(*args, **kwargs)

class CommunityDoc(models.Model):
    document_id = models.AutoField(primary_key=True)
    community_id = models.ForeignKey(Community, on_delete=models.CASCADE)
    created_date = models.DateField(auto_now_add=True)
    created_user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=255, blank=True, null=True)
    title = models.CharField(max_length=100) 
    doc_cid = models.TextField(max_length=255, null=False, blank=True)
    price = models.IntegerField(default=0, validators=[validate_no_negative])
    
    # def save(self, *args, **kwargs):
    #     if not self.pk:
    #         self.doc_cid = encrypt(self.doc_cid)
    #         super(CommunityDoc, self).save(*args, **kwargs)


class CommunityCerti(models.Model):
    id = models.AutoField(primary_key=True)
    certificate_type_id = models.IntegerField()
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    gained_date = models.DateField(auto_now_add=True)
    title = models.CharField(max_length=100) 
    community_id = models.ForeignKey(Community, on_delete=models.CASCADE)
    description = models.CharField(max_length=255, blank=True, null=True)

    def save(self, *args, **kwargs):
        # Get the day, month, and year from the created_date
        day = str(self.gained_date.day).zfill(2)
        month = str(self.gained_date.month).zfill(2)
        year = str(self.gained_date.year % 100).zfill(2)

        # Concatenate community_id and formatted created_date to generate commu_history_id
        self.id = f"{self.certificate_type_id}-{self.user_id}-{day}{month}{year}"

        super().save(*args, **kwargs)

class CommunityFormer(models.Model):
    id = models.AutoField(primary_key=True)
    community_id = models.ForeignKey(Community, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        # Concatenate community_id and formatted created_date to generate commu_history_id
        self.id = f"{self.community_id}_{self.user_id}"

        super().save(*args, **kwargs)

# class CommunityMember(models.Model):
    
#     community= models.ForeignKey(Community, on_delete=models.CASCADE)
#     member= models.ForeignKey(User, on_delete=models.CASCADE)
#     date_joined = models.DateField(auto_now_add=True)
#     is_mentor = models.BooleanField(default=False)
#     point= models.IntegerField(default=0)

#     def save(self, *args, **kwargs):
#     # Get the day, month, and year from the created_date
#         day = str(self.date_joined.day).zfill(2)
#         month = str(self.date_joined.month).zfill(2)
#         year = str(self.date_joined.year % 100).zfill(2)

#         # self.id = f"{self.community}-{self.member}-{day}{month}{year}"

#         super().save(*args, **kwargs)

class CommunityQuiz(models.Model):
    id = models.AutoField(primary_key=True)
    community_id = models.ForeignKey(Community, on_delete=models.CASCADE)
    creator_id = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    value = models.IntegerField(default=0, validators=[validate_no_negative])
    passing_score = models.FloatField() 

    def __str__(self):
        return str(self.title) + '-' + str(self.community_id)
    
    def get_questions(self):
        return self.question_set.all()

class Question(models.Model):
    id = models.AutoField(primary_key=True)
    quiz_id = models.ForeignKey(CommunityQuiz, on_delete=models.CASCADE)
    text = models.CharField(max_length=100)

    def __str__(self):
        return str(self.text)

    def get_answers(self):
        return self.answer_set.all()

class Answer(models.Model):
    text = models.CharField(max_length=100)
    is_correct = models.BooleanField(default=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    def __str__(self):
        return str("question " + self.question.text) + '-' + str("answer" + self.text)