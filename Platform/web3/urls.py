from django.contrib import path
from .views import *

urlpatterns = [
    path('', home, name="home"),
]

# Register your models here.
