from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name="home"),
    path('home', home, name="home"),
    path('community/<int:pk>', community_detail, name='community-detail'),
    path('community-interface/home/<int:pk>', community_interface, name='community-interface'),
    path('community-interface/mentor/<int:pk>', community_mentor, name='community-mentor'),
    path('community-interface/setting/<int:pk>', community_setting, name='community-setting'),
    path('community-interface/docs/<int:pk>', get_community_docments, name='community-docs'),
    path('community-interface/exam/<int:pk>', get_community_exam, name='community-exam'),
    path('add-community', add_community, name='add-community'),
    path('done_exam', done_exam, name='done-exam'),
    path('back_home_from_exam', back_community, name='back-community'),
    path('request-mentor', request_mentor, name='ajax-request-mentor'),
    path('join-community/<int:pk>', join_community, name='join-community'),
    path('join-community/<int:pk>/<int:userId>', join_community, name='join-community-exam'),
    path('verify-exam-score', verify_exam, name='verify-exam'),
    path('synchronize_data', synchronize_data, name='synchronize-data'),
]