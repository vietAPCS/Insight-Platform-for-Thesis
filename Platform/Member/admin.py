from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(UserCommunity),
admin.site.register(MyUser),
admin.site.register(UserHistory),
admin.site.register(RequestMentor),

