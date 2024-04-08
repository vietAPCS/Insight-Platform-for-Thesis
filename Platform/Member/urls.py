from django.urls import path
from .views import *

urlpatterns = [
    path('login', signin, name='signin'),
    path('signup', signup, name='signup'),
    path('signout', signout, name='signout'),
    path('profile/<int:pk>', profile, name='profile'),
    path('profile/edit/<int:pk>', edituser, name='edituser')
]