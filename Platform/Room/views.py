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
    this_community_user = UserCommunity.objects.get(
            user_id=this_user, 
            community_id=community)
    isMember = Validate_member(this_user, community)

    if not isMember:
        return redirect('Community:home')
    elif request.POST.get('new_score', False):
        new_score = request.POST.get('new_score')
        mentors_community = UserCommunity.objects.filter(community_id=community, is_mentor = True, score__gte = new_score).exclude(user_id = this_user)
        mentors_community = mentors_community.order_by("?")[:3]
        
        new_room = ExamRoom()
        new_room.prev_grade = this_community_user.score
        new_room.wanted_grade = new_score
        new_room.community_id = community
        new_room.student_id = this_user
        new_room.save()

        for m in mentors_community:
            new_room.detail.add(m.user_id)
        
        return redirect('Room:room_details', com_id=community.id, room_id=new_room.id)
    
    else:
        # isFormer = Validate_former(this_user, community)
        this_community_user = UserCommunity.objects.get(
            user_id=this_user, community_id=community)
        mentors_community = UserCommunity.objects.filter(community_id=community, is_mentor = True)
        mentors_community = mentors_community.order_by('-score')
        context = {
            'user': this_community_user,
            'community': community,
            # 'is_former': isFormer,
            'mentors': mentors_community,
        }
        return render(request, 'Room/contest.html', context)
    

def room_details(request, com_id, room_id):
    if not request.user.is_authenticated:
        return redirect('Member:signin')

    this_user = request.user
    community = Community.objects.get(id=com_id)
    isMember = Validate_member(this_user, community)
    if not isMember:
        return redirect('Community:home')
    else:
        room = ExamRoom.objects.get(id=room_id)
        room_detail = RoomDetails.objects.filter(room_id=room_id)
        context = {
            'room': room,
            'community': community,
            'room_details': room_detail,
        }
        return render(request, 'Room/render_room.html', context)
    
