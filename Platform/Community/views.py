from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.conf import settings
from .models import *
from django.views.generic import ListView, DetailView, CreateView
from .forms import CommunityForm
from Member.models import *
from datetime import datetime
import requests
from Platform.utils import *
import json
import pandas as pd
# Create your views here.


def community_interface(request, pk):
    pass


def home(request):
    if not request.user.is_authenticated:
        return redirect('Member:signin')
    else:
        # select * from community
        this_user = request.user
        all_communities = Community.objects.all()
        flag = False if len(all_communities) == 0 else True
        joined_community = UserCommunity.objects.filter(
            user_id=this_user).all()

        context = {
            'flag': flag,
            'communities': all_communities,
            'shorcuts': joined_community
        }
        return render(request, 'Community/home.html', context)

def Validate_member(user, community):
    isMember = UserCommunity.objects.filter(
        user_id=user, community_id=community).exists()
    return isMember

def Validate_mentor(user, community):
    isMentor = UserCommunity.objects.filter(
        user_id=user, community_id=community, is_mentor=True).exists()
    return isMentor


def Validate_former(user, community):
    isFormer = Community.objects.filter(created_user_id=user,id=community.id).exists()
    return isFormer


def community_interface(request, pk):
    if not request.user.is_authenticated:
        return redirect('Member:signin')

    this_user = request.user
    community = Community.objects.get(id=pk)
    isMember = Validate_member(this_user, community)
    if not isMember:
        return redirect('Community:community-detail', pk=pk)
    else:
        isFormer = Validate_former(this_user, community)
        this_community_user = UserCommunity.objects.get(
            user_id=this_user, community_id=community)
        user_img = MyUser.objects.get(userid = this_user).avatar
        users_community = UserCommunity.objects.prefetch_related('user_id__myuser').filter(community_id=community)
        users_community = users_community.order_by('-score')
        context = {
            'this_c_user': this_community_user,
            'community': community,
            'is_former': isFormer,
            'users_community': users_community,
            'img': user_img
        }
        return render(request, 'Community/community_interface.html', context)


def community_detail(request, pk):
    if not request.user.is_authenticated:
        return redirect('Member:signin')
    else:
        community = Community.objects.get(id=pk)
        user = request.user
        isMember = Validate_member(user, community)
        community_size = UserCommunity.objects.filter(
                community_id=pk).count()
        num_documents = CommunityDoc.objects.filter(
            community_id=pk).count()
        num_mentors = UserCommunity.objects.filter(
            community_id=pk, is_mentor=True).count()
        context = {
            "community_size": community_size,
            "num_documents": num_documents,
            "num_mentors": num_mentors,
            "community": community,
            "user": user,
            'ismember': isMember,
        }
        return render(request, 'Community/community_detail.html', context)

def community_mentor(request, pk):
    if not request.user.is_authenticated:
        return redirect('Member:signin')
    else:
        this_user = request.user
        community = Community.objects.get(id=pk)
        isMember = Validate_member(this_user, community)
        if not isMember:
            return redirect('Community:community-detail', pk=pk)
        else:
            this_community_user = UserCommunity.objects.prefetch_related('user_id__myuser').get(
                user_id=this_user, community_id=community)
            user_img = MyUser.objects.get(userid = this_user).avatar
            isFormer = Validate_former(this_user, community)
            threshold = community.mentor_threshold
            mentor = UserCommunity.objects.prefetch_related('user_id__myuser').filter(community_id=community, is_mentor=True)
            context = {
                'this_c_user': this_community_user,
                'community_mentors': mentor,
                'community': community,
                'is_former': isFormer,
                'img': user_img
            }
            return render(request, 'Community/community_mentor.html', context)


def community_setting(request, pk):
    if not request.user.is_authenticated:
        return redirect('Member:signin')
    else:
        this_user = request.user
        community = Community.objects.get(id=pk)
        is_former = Validate_former(this_user, community)
        if not is_former:
            return redirect('Community:community-detail', pk=pk)
        else:
            if request.method == 'POST':
                community_name = request.POST['community-name']
                update_community = Community.objects.get(id=pk)
                update_community.name = community_name

                community_description = request.POST['community-description']
                update_community.description = community_description

                community_threshold = request.POST['community-threshold']
                update_community.mentor_threshold = community_threshold

                community_upload_permission = request.POST['community-upload-permission']
                update_community.upload_permission = community_upload_permission

                if 'enable-entrance-test' in request.POST:
                    enable_entrance_test = request.POST['enable-entrance-test']
                    if enable_entrance_test == 'on':
                        update_community.entrance_test_enable = True
                else:
                    update_community.entrance_test_enable = False

                update_community.save()
                print(update_community)
                print(update_community.mentor_threshold)
                return JsonResponse(request.POST)
            else:
                community = Community.objects.get(id=pk)
                this_user = request.user
                user_img = MyUser.objects.get(userid = this_user).avatar
                this_community_user = UserCommunity.objects.get(
                    user_id=this_user, community_id=community)
                print(this_user)
                context = {
                    'this_c_user': this_community_user,
                    'is_former': is_former,
                    'community': community,
                    'img': user_img
                }
                print(community.upload_permission)
                return render(request, 'Community/community_setting.html', context)

def request_mentor(request):
    if not request.user.is_authenticated:
        return redirect('Member:signin')
    else:
        usercommunityID = request.GET.get('user_communityID')
        mentorID = request.GET.get('mentorID')
        communityID = request.GET.get('communityID')
        community = Community.objects.get(id=communityID)
        flag = True
        status = None
        err_message = ""
        if not community:
            flag = False
            err_message = "Community not found"
        else:
            # Initialize flag and status
            # Check foreign key reference
            requesting_user = UserCommunity.objects.get(
                id=usercommunityID, community_id=community)
            requested_mentor = UserCommunity.objects.get(
                id=mentorID, community_id=community)

            if requested_mentor == None or requesting_user == None:
                flag = False
                err_message = "user or mentor not exist"
            else:
                print(requested_mentor)
                print(requesting_user)
                # Check if a record with the same usercommunityID and mentorID exists
                existing_request = RequestMentor.objects.filter(
                    UserCommunityId=requesting_user,
                    mentorId=requested_mentor
                ).exists()

                self_request = requesting_user == requested_mentor

                if existing_request:
                    # If a record exists, set flag to False and retrieve status
                    flag = False
                    err_message = "request exit"
                elif self_request:
                    flag = False
                    status = existing_request.status
                    err_message = "can not request yourself"
                else:
                    print("tesssstt")
                    record = RequestMentor(
                        UserCommunityId=requesting_user,
                        mentorId=requested_mentor,
                        status=0,
                    )
                    status = 0
                    record.save()

        # Create a JSON response
        response_data = {
            'flag': flag,
            'status': status,
            'err_message': err_message
        }

        return JsonResponse(response_data)

def ansewer_request_mentor(request):
    if request.method == "POST":
        # Retrieve usercommunityID, mentorID, and option from POST data
        usercommunityID = request.POST.get('...')
        mentorID = request.POST.get('...')
        option = request.POST.get('...')

        # Check if a record with the same usercommunityID and mentorID exists
        existing_request = RequestMentor.objects.filter(
            UserCommunityId=usercommunityID,
            mentorId=mentorID
        ).first()

        # Initialize flag
        flag = True

        if not existing_request:
            # If no record exists, set flag to False
            flag = False
        else:
            # Check foreign key reference
            requesting_user = UserCommunity.objects.filter(id=usercommunityID)
            requested_mentor = UserCommunity.objects.filter(
                user_id=mentorID).first()
            if (requested_mentor != None and requesting_user != None):
                # If a record exists, update the status based on the option
                if option == 1:
                    existing_request.status = 1  # Accept
                elif option == 2:
                    existing_request.status = 2  # Reject
                else:
                    flag = False
                    return JsonResponse({'error': 'Invalid option'})
                existing_request.save()

        # Create a JSON response
        response_data = {
            'usercommunityID': usercommunityID,
            'mentorID': mentorID,
            'status': option,
            'flag': flag
        }

        return JsonResponse(response_data)
    else:
        # Handle other HTTP methods (e.g., GET)
        return JsonResponse({'error': 'Invalid request method'}, status=405)


def upload_document(request, pk):
    this_user = request.user
    community = Community.objects.get(id=pk)
    isMember = Validate_member(this_user, community)
    isMentor = Validate_mentor(this_user, community)
    isFormer = Validate_former(this_user, community)
    
    if not request.user.is_authenticated:
        return redirect('Member:signin')
    elif not isMember:
            redirect('Community:community-detail', pk=pk)
    elif ((community.upload_permission==1) or 
        (((isFormer or isMentor) and community.upload_permission==2)) or
        (isFormer and community.upload_permission==3)):

        if request.method == 'POST':
            title = request.POST['title']
            description = request.POST['description']
            price = request.POST['price']
            new_doc = CommunityDoc()
            new_doc.title = title
            new_doc.description = description
            new_doc.created_user_id = this_user
            new_doc.created_date = datetime.now()
            new_doc.community_id = community
            new_doc.price = price
            new_doc.doc_cid = get_cid(request)

            new_doc.save()
            
            return redirect('Community:community-docs', pk=pk)
        else:
            community = Community.objects.get(id=pk)
            this_user = request.user
            myuser = MyUser.objects.get(userid = this_user)
            this_community_user = UserCommunity.objects.get(
                user_id=this_user, community_id=community)
            print(this_user)
            context = {
                    'this_c_user': this_community_user,
                    'is_former': isFormer,
                    'community': community,
                    'img': myuser.avatar,
                    'metamask_id': myuser.metamaskID
                }
            return render(request, 'Community/upload_doc.html', context)
    else:
        return community_interface(request, pk)

# get document and return render html
def get_community_docments(request, pk):
    if not request.user.is_authenticated:
        return redirect('Member:signin')
    else:
        this_user = request.user
        community = Community.objects.get(id=pk)
        isMember = Validate_member(this_user, community)
        isMentor = Validate_mentor(this_user, community)
        isFormer = Validate_former(this_user, community)
        if not isMember:
            redirect('Community:community-detail', pk=pk)
        elif request.POST.get('download', False):
            return get_file(request)
        else:
            community_docs = CommunityDoc.objects.prefetch_related('created_user_id__myuser').filter(
                community_id=community).all()
            this_community_user = UserCommunity.objects.prefetch_related('user_id__myuser').get(
                user_id=this_user, community_id=community)
            user_img = MyUser.objects.get(userid = this_user).avatar

            can_upload = False
            if ((community.upload_permission==1) or 
                (((isFormer or isMentor) and community.upload_permission==2)) or
                (isFormer and community.upload_permission==3)):
                can_upload = True

            context = {
                'community': community,
                'this_c_user': this_community_user,
                'community_docs': community_docs,
                'is_former': isFormer,
                'can_upload': can_upload,
                'img': user_img
            }
            return render(request, 'Community/community_document.html', context)


def add_community(request):
    if not request.user.is_authenticated:
        return redirect('Member:signin')
    else:
        user = request.user
        if request.method == 'POST':
            name = request.POST.get('community-name')
            description = request.POST.get('community-description')
            mentor_thres = request.POST.get('mentor-threshold')
            upload_permit = request.POST.get('community-upload-permission')
            entrance_test_enable = request.POST.get('enable-entrance-test')

            new_community = Community()
            new_community.name = name
            new_community.description = description
            new_community.created_user = user
            new_community.mentor_threshold = mentor_thres
            new_community.upload_permission = upload_permit
            if (entrance_test_enable == 'on'):
                new_community.entrance_test_enable = 1

            new_community.save()
            new_userCommunity = UserCommunity()
            new_userCommunity.user_id = user
            new_userCommunity.community_id = new_community
            new_userCommunity.is_mentor = False
            new_userCommunity.save()
            # if (entrance_test_enable == 'on'):
            # return redirect('Community:entrance_test') Hưng làm tiếp chỗ này
            return redirect('Community:home')
        return render(request, 'Community/add_community.html')


def join_community(request, pk, userId=None):
    community = Community.objects.get(id=pk)
    # nếu có bật chức năng test thì chuyển qua trang test của nhóm khác
    if community.entrance_test_enable:
        return redirect('Community:home')
    else:
        user = request.user
        if request.user.is_authenticated:
            # community.Member.add(user)
            # community.save()
            user_community = UserCommunity()
            user_community.user_id = user
            user_community.community_id = community
            # user_community.score=10
            user_community.save()
            return redirect('Community:community-detail', pk=pk)

def quiz_list(request, pk):
    if not request.user.is_authenticated:
        return redirect('Member:signin')
    else:
        this_user = request.user
        community = Community.objects.get(id=pk)
        isMember = Validate_member(this_user, community)
        isMentor = Validate_mentor(this_user, community)
        isFormer = Validate_former(this_user, community)
        
        isCreateQuizzes = False
        if (community.upload_permission == 1 or 
            (community.upload_permission == 2 and isMentor) or 
            (community.upload_permission == 2 and isFormer) or 
            (community.upload_permission == 3 and isFormer)):
            isCreateQuizzes = True
        if not isMember:
            redirect('Community:community-detail', pk=pk)
        else:
            this_community_user = UserCommunity.objects.prefetch_related('user_id__myuser').get(
                user_id=this_user, community_id=community)
            user_img = MyUser.objects.get(userid = this_user).avatar
            community_quizzes = CommunityQuiz.objects.filter(
            community_id=pk).all()

            context = {
                'community':community,
                'community_quizzes': community_quizzes,
                'isCreateQuizzes': isCreateQuizzes,
                'this_c_user': this_community_user,
                'img': user_img,
                'is_former': isFormer,
            }
            return render(request, 'Community/quiz_list.html', context)    
        
def upload_quiz(request, pk):
    this_user = request.user
    community = Community.objects.get(id=pk)
    isMember = Validate_member(this_user, community)
    isMentor = Validate_mentor(this_user, community)
    isFormer = Validate_former(this_user, community)
    
    if not request.user.is_authenticated:
        return redirect('Member:signin')
    elif not isMember:
            redirect('Community:community-detail', pk=pk)

    elif ((community.upload_permission==1) or 
        (((isFormer or isMentor) and community.upload_permission==2)) or
        (isFormer and community.upload_permission==3)):

        tsd = ['A', 'B', 'C', 'D']
        if request.method == 'POST':
            if(len(request.FILES) != 0):
                title = request.POST['title']
                pass_score = request.POST['pass_score']
                value = request.POST['price']
                new_quiz = CommunityQuiz()
                new_quiz.title = title
                new_quiz.creator_id = this_user
                new_quiz.value = value
                new_quiz.passing_score = pass_score
                new_quiz.community_id = community
                new_quiz.save()

                file = request.FILES['doc']
                file_extension = file.name.split('.')

                if file_extension[1] == 'xlsx':
                    df = pd.read_excel(file, engine='openpyxl')
                elif file_extension[1] == 'xls':
                    df = pd.read_excel(file)
                elif file_extension[1] == 'csv':
                    df = pd.read_csv(file)
                else:
                    raise Exception("File not supported")
                try:
                    for index, row in df.iterrows():
                        question = row['Question']
                        print(question)
                        q = Question()
                        q.quiz_id = new_quiz
                        q.text = question
                        q.save()
                        for t in tsd:
                            ans = Answer()
                            ans.question = q
                            ans.text = row[t]
                            if t == row['Correct']:
                                ans.is_correct = True
                                print(row[t]+"-correct")
                            else:
                                print(row[t])
                            ans.save()
                except:
                    raise Exception("Wrong file format")
                
            return redirect('Community:quiz-list', pk=pk)
        else:
            community = Community.objects.get(id=pk)
            this_user = request.user
            myuser = MyUser.objects.get(userid = this_user)
            this_community_user = UserCommunity.objects.get(
                user_id=this_user, community_id=community)
            print(this_user)
            context = {
                'this_c_user': this_community_user,
                'is_former': isFormer,
                'community': community,
                'img': myuser.avatar,
                'metamask_id': myuser.metamaskID,
            }
            return render(request, 'Community/upload_quiz.html', context)
    else:
        return community_interface(request, pk)

def quiz(request, pk, quiz_id):
    
    quiz = CommunityQuiz.objects.get(id=quiz_id)
    this_user = request.user
    community = Community.objects.get(id=pk)
    isMember = Validate_member(this_user, community)
    isFormer = Validate_former(this_user, community)

    try:
        quiz_complete = QuizComplete.objects.get(quiz_id=quiz_id, user_id=this_user).is_complete
    except QuizComplete.DoesNotExist:
        quiz_complete = False

    if not request.user.is_authenticated:
        return redirect('Member:signin')
    elif not isMember:
        return redirect('Community:community-detail', pk=pk)
    elif request.method == 'POST':
        answers = request.POST.dict()
        score = 0
        for key, value in answers.items():
            a = Answer.objects.get(id=value)
            if(a.is_correct):
                score+=1
        result = ""
        if score >= quiz.passing_score:
            result = "Passed"
            if not quiz_complete:
                new_quiz_complete = QuizComplete()
                new_quiz_complete.quiz_id = quiz
                new_quiz_complete.user_id = this_user
                new_quiz_complete.is_complete = True
                new_quiz_complete.save()
        else: 
            result = "Failed"
        return JsonResponse({'result': result, 'complete': quiz_complete})

    questions = Question.objects.prefetch_related("answer_set").filter(quiz_id=quiz).all()

    community = Community.objects.get(id=pk)
    this_user = request.user
    myuser = MyUser.objects.get(userid = this_user)
    this_community_user = UserCommunity.objects.get(
        user_id=this_user, community_id=community)
    
    context = {
        'this_c_user': this_community_user,
        'is_former': isFormer,
        'community': community,
        'img': myuser.avatar,
        'metamask_id': myuser.metamaskID,
        'questions': questions,
        'quiz': quiz,
    }
    return render(request, 'Community/quiz.html', context)
