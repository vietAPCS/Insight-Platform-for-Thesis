from itertools import count
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from .models import *
from django.contrib.auth.models import User
from datetime import datetime
# Create your views here.

def signin(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(username=username, password=password)
            print(username, password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('Community:home')
                else:
                    return redirect('Member:signin')
            else :
                return render(request, 'Member/signin.html', {})
        else:
            return render(request, 'Member/signin.html')
    else:
        return redirect('Community:home')

def signup(request):
    if not request.user.is_authenticated:

        if request.method == 'POST':
            username = request.POST.get('username', None)
            password = request.POST.get('password', None)
            password2 = request.POST.get('password2', None)
            metamarskID = request.POST.get('metamarsk-id')

            if password != password2:
                return render(request, 'Member/signup.html')
            
            new_user = User()
            new_user.username = username
            print(username, password)
            new_user.set_password(password)
            new_user.date_joined = datetime.now()
            new_user.is_active = True
            new_user.save()

            new_my_user = MyUser()
            new_my_user.userid = new_user
            new_my_user.MetamarskID = metamarskID
            new_my_user.save()
    
            login(request, new_user)
            return redirect('Community:home')
        else:
            return render(request, 'Member/signup.html')  
    else:
        return render(request, 'Community/home.html')  

def signout(request):
    logout(request)
    return redirect('Member:signin')

def profile(request, pk):
    if not request.user.is_authenticated:
        return redirect('Member:signin')
    else:
        this_user = User.objects.get(id = pk)
        this_user2 = User.objects.get(id = pk)
        # print(this_user)
        user_communities = UserCommunity.objects.filter(user_id = this_user)
        creater_communities = Community.objects.filter(created_user = this_user)
        len = []
        for i in creater_communities:
            len.append(
                { 
                    "community": i,
                    "len": UserCommunity.objects.filter(community_id = i).count()	
                }
            )
        print(len)
        context = {
            'this_user': this_user,
            'user_communities': user_communities,
            'creater_communities': creater_communities,
            "len": len
        }
        
        return render(request, 'Member/profile.html', context)
    

def edituser(request, pk):
    if not request.user.is_authenticated:
        return redirect('Member:signin')
    else:
        user = request.user
        this_user = User.objects.get(id = pk)
        if user != this_user:
            return render(request, 'Member/error.html')
        else:
            if request.method == 'POST':
                pass
            else:
                return render(request, 'Member/edit_user.html')