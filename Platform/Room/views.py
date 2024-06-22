from itertools import count
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from .models import *
from Member.models import *
from Community.models import *
from Community.views import Validate_former, Validate_member
from django.contrib.auth.models import User
from datetime import datetime
from Platform.utils import *


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
            'current_user': this_user,
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
    elif request.method == 'POST':
        if request.POST.get('download', False):
            return get_file(request)
    else:
        room = ExamRoom.objects.get(id=room_id)
        room_detail = RoomDetails.objects.filter(room_id=room_id)
        context = {
            'room': room,
            'community': community,
            'room_details': room_detail,
            'current_user': this_user,
        }
        return render(request, 'Room/render_room.html', context)
    
def profile(request, com_id, user_id):
    if not request.user.is_authenticated:
        return redirect('Member:signin')

    this_user = user_id
    user = MyUser.objects.get(userid=this_user)
    community = Community.objects.get(id=com_id)
    this_community_user = UserCommunity.objects.get(
            user_id=this_user, 
            community_id=community,
            )
    isMember = Validate_member(request.user, community)

    if not isMember:
        return redirect('Community:home')
    else:
        room = ExamRoom.objects.filter(student_id=this_user)
        # room_detail = RoomDetails.objects.filter(room_id=room)
        context = {
            'metamask': user.metamaskID,
            'user': this_community_user,
            'rooms': room,
            'community': community,
            'current_user': request.user,
            # 'room_details': room_detail,
        }
        return render(request, 'Room/user_profile.html', context)

def former(request, com_id):
    if not request.user.is_authenticated:
        return redirect('Member:signin')

    this_user = request.user
    community = Community.objects.get(id=com_id)
    isMember = Validate_member(this_user, community)
    is_former = Validate_former(this_user, community)

    if not isMember:
        return redirect('Community:home')
    elif not is_former:
        return render(request, 'Room/403.html', {'community': community})
    elif request.method == 'POST' and request.POST.get('id', False):
        if request.POST.get('signature', False):
            room_id = request.POST['id']
            signature = request.POST['signature']
            room = ExamRoom.objects.get(id=room_id)
            room.former_signature = signature
            room.save(update_fields=["former_signature"])
            return JsonResponse({'ok': 'yes'})
        
        if request.POST.get('signing', False):
            room_id = request.POST['id']
            room = ExamRoom.objects.get(id=room_id)
            room_details = RoomDetails.objects.filter(room_id=room)
            string =""
            for test in room_details:
                string = string + str(test.grade).zfill(2)
            string = string + str(room.prev_grade).zfill(2) + str(room.final_grade).zfill(2)
            return JsonResponse({'ok': string})
        
    else:
        room = ExamRoom.objects.filter(community_id=community)
        # room_detail = RoomDetails.objects.filter(room_id=room)
        context = {
            'rooms': room,
            'community': community,
            'current_user': this_user,
            # 'room_details': room_detail,
        }
        return render(request, 'Room/former_view.html', context)

def mentor(request, com_id):
    if not request.user.is_authenticated:
        return redirect('Member:signin')

    this_user = request.user
    community = Community.objects.get(id=com_id)
    isMember = Validate_member(this_user, community)

    if not isMember:
        return redirect('Community:home')
    
    elif request.method == 'POST':
        if request.POST.get('download', False):
            return get_file(request)
        if request.POST.get('id', False):
            if request.POST.get('score', False) and request.POST.get('score_signature', False):
                detail_id = request.POST['id']
                room_detail = RoomDetails.objects.get(id=detail_id)
                # .update(mentor_signature=signature, score_signature=score_signature)
                score = float(request.POST['score'])
                score_signature = request.POST['score_signature']

                room_detail.grade = score
                room_detail.score_signature = score_signature

                room_detail.save(update_fields=["grade", "score_signature"])
                cal_final_grade(room_detail.room_id)
                return JsonResponse({'ok': 'yes'})
            
            if request.FILES.get('doc', False):
                detail_id = request.POST['id']
                cid = get_cid(request)
                room_detail = RoomDetails.objects.get(id=detail_id)
                room_detail.exam_cid = cid
                room_detail.save(update_fields=["exam_cid"])
                return JsonResponse({'cid': room_detail.exam_cid})

            if request.POST.get('signature', False):
                detail_id = request.POST['id']
                signature = request.POST['signature']
                room_detail = RoomDetails.objects.filter(id=detail_id).update(mentor_signature=signature)
                return JsonResponse({'ok': 'yes'})
    
    else:
        room_detail = RoomDetails.objects.filter(mentor_id=this_user)
        # room = ExamRoom.objects.get(student_id=this_user)
        context = {
            # 'room': room,
            'community': community,
            'room_details': room_detail,
            'current_user': this_user,
        }
        return render(request, 'Room/mentor.html', context)
    
def contestant_details(request, com_id, room_id):
    if not request.user.is_authenticated:
        return redirect('Member:signin')

    this_user = request.user
    community = Community.objects.get(id=com_id)
    room = ExamRoom.objects.get(id=room_id)
    isMember = Validate_member(this_user, community)
    
    if not isMember:
        return redirect('Community:home')
    elif this_user != room.student_id:
        return redirect('Room:room_details', com_id=com_id, room_id=room_id)
    elif request.method == 'POST':
        if request.POST.get('download', False):
            return get_file(request)    
        
        if request.FILES.get('doc', False) and request.POST.get('id', False):
            detail_id = request.POST['id']
            cid = get_cid(request)
            room_detail = RoomDetails.objects.get(id=detail_id)
            room_detail.answer_cid = cid
            room_detail.save(update_fields=["answer_cid"])
            return JsonResponse({'cid': room_detail.answer_cid})

        if request.POST.get('signature', False) and request.POST.get('id', False):
            detail_id = request.POST['id']
            signature = request.POST['signature']
            room_detail = RoomDetails.objects.filter(id=detail_id).update(student_signature=signature)
            return JsonResponse({'ok': 'yes'})
    else:
        room_detail = RoomDetails.objects.filter(room_id=room_id)
        context = {
            'room': room,
            'community': community,
            'room_details': room_detail,
            'current_user': this_user,
        }
        return render(request, 'Room/render_contestant_room.html', context)

def cal_final_grade(room):
    score = 0
    room_details = RoomDetails.objects.filter(room_id=room)

    for a in room_details:
        if not a.score_signature:
            return
        score += a.grade
    score = score/room_details.count()
    final_grade = score * (room.wanted_grade-room.prev_grade)

    final_grade = final_grade / 100

    room.final_grade = final_grade + room.prev_grade
    room.save(update_fields=["final_grade"])