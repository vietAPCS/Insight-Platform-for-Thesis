from itertools import count
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from .models import *
from Member.models import *
from Community.models import *
from Community.views import Validate_former, Validate_member
from django.contrib.auth.models import User
from datetime import datetime

# Create your views here.
def contest(request, pk):
    if not request.user.is_authenticated:
        return redirect('Member:signin')

    this_user = request.user
    community = Community.objects.get(id=pk)
    isMember = Validate_member(this_user, community)
    if not isMember:
        return redirect('Community:home')
    else:
        isFormer = Validate_former(this_user, community)
        this_community_user = UserCommunity.objects.get(
            user_id=this_user, community_id=community)
        mentors_community = UserCommunity.objects.filter(community_id=community, is_mentor = False)
        mentors_community = mentors_community.order_by('-score')
        context = {
            'user': this_community_user,
            'community': community,
            'is_former': isFormer,
            'mentors': mentors_community,
        }
        return render(request, 'Room/contest.html', context)
    
def room_render(request, pk):
    community = Community.objects.get(id=pk)
    context = {    
            'community': community,
        }
    return render(request, 'Room/upload_file_render.html', context)