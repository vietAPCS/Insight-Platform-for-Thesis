from django.urls import path
from .views import *

urlpatterns = [
    path('general', home2, name="home2"),
]

# Register your models here.
