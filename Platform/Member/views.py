from itertools import count
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from .models import *
from django.contrib.auth.models import User
from datetime import datetime
import requests
from django.http import HttpResponse
from Platform.utils import *
import os
#from .forms import *
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
            metamaskID = request.POST.get('metamaskID', None)

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
            new_my_user.metamaskID = metamaskID
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
        user_img = MyUser.objects.get(userid = this_user).avatar
        metamaskID = MyUser.objects.get(userid = this_user).metamaskID
        user_communities = UserCommunity.objects.filter(user_id = this_user)
        creater_communities = Community.objects.filter(created_user = this_user)
        infura_key= os.environ.get('INFURA_API_KEY')
        private_key = os.environ.get('SIGNER_PRIVATE_KEY')
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
            'metamaskID': metamaskID,
            "len": len,
            'img': user_img,
            'infura_key': infura_key,
            'private_key': private_key
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
            user2 = MyUser.objects.get(userid = this_user)
            if request.method == 'POST':
                username = request.POST.get('nick-name', None)
                metamaskID = request.POST.get('metamaskID', None)
                if(len(request.FILES)!=0):
                    user2.avatar = request.FILES['image']
                    user2.metamaskID = metamaskID
                    user2.save()

                this_user.username = username
                this_user.save()
                return redirect('/')
            else:
                context = {
                    'user_name':this_user.username,
                    'metamaskID':user2.metamaskID,
                    'img':user2.avatar,
                }
                return render(request, 'Member/edit_user.html',context)
