from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('contest/<int:pk>', contest, name='contest'),
    path('contest/<int:com_id>/profile/<int:user_id>', profile, name='profile'),
    path('contest/<int:com_id>/mentor', mentor, name='mentor'),
    path('contest/<int:com_id>/former', former, name='former'),
    path('contest/<int:com_id>/<int:room_id>', room_details, name='room_details'),
    path('contest/<int:com_id>/<int:room_id>-contestant', contestant_details, name='contestant_details'),
]