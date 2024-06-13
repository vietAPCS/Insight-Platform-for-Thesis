from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('contest/<int:pk>', contest, name='contest'),
    path('contest/<int:com_id>/<int:room_id>', room_details, name='room_details')
    # path('mentor/<int:pk>', mentor, name='mentor'),
]