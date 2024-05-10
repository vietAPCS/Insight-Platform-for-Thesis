from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('contest/<int:pk>', contest, name='contest'),
    path('contest/room_render/<int:pk>', room_render, name='room_render'),
    # path('mentor/<int:pk>', mentor, name='mentor'),
]