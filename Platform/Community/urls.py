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
    path('community-interface/upload_doc/<int:pk>', upload_document, name='upload_doc'),
    path('add-community', add_community, name='add-community'),
    path('request-mentor', request_mentor, name='ajax-request-mentor'),
    path('join-community/<int:pk>', join_community, name='join-community'),
    path('join-community/<int:pk>/<int:userId>', join_community, name='join-community-exam'),
    path('community-interface/quiz-list/<int:pk>', quiz_list, name='quiz-list'),
    path('community-interface/upload_quiz/<int:pk>', upload_quiz, name='upload-quiz'),
    path('community-interface/quiz/<int:pk>/<int:quiz_id>', quiz, name='quiz'),
]