from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
def home(request):
    return HttpResponse('Login page')
    # if request.method == 'POST':
    #     username = request.POST.get('username')
    #     password = request.POST.get('password')
    #     user = authenticate(request, username=username, password=password)
    #     if user is not None:
    #         login(request, user)
    #         return HttpResponse('Login successful')
    #     else:
    #         return HttpResponse('Invalid credentials')
    # else:
    #     return render(request, 'login.html')
# Create your views here.
