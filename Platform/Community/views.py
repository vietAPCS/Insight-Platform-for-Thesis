from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import *
from django.views.generic import ListView, DetailView, CreateView
from .forms import CommunityForm
from Member.models import *
import requests
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


#################
#
# với mỗi hàm cần làm thì hoàn thiện lun path trong file url.py
#
# ##########
def Validate_member(user, community):
    isMember = UserCommunity.objects.filter(
        user_id=user, community_id=community).exists()
    return isMember


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
        this_community_user = UserCommunity.objects.filter(
            user_id=this_user, community_id=community)
        users_community = UserCommunity.objects.filter(community_id=community)
        users_community = users_community.order_by('-score')
        print(community)
        context = {
            'this_c_user': this_community_user,
            'community': community,
            'is_former': isFormer,
            'users_community': users_community,
        }
        # context['community_size'] = creater_communities.count()
        return render(request, 'Community/community_interface.html', context)


def community_detail(request, pk):
    if not request.user.is_authenticated:
        return redirect('Member:signin')
    else:
        community = Community.objects.get(id=pk)
        user = request.user
        isMember = Validate_member(user, community)
        if isMember == True:
            return redirect('Community:community-interface', pk=pk)
        else:
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
            }
            return render(request, 'Community/community_detail.html', context)

# 1. xác định người dùng có thuộc community hay ko, nếu ko thì redirect qua trang detail
# 2. xác định người dùng có phải former hay ko
# 3. truy vấn ra danh sách tất cả các mentor thuộc community
# 4. render trang communitymentor


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
            this_community_user = UserCommunity.objects.filter(
                user_id=this_user, community_id=community)
            isFormer = Validate_former(this_user, community)
            threshold = community.mentor_threshold
            mentor = UserCommunity.objects.filter(
                community_id=community, score__gt=threshold)
            context = {
                'this_c_user': this_community_user,
                'community_mentors': mentor,
                'community': community,
                'is_former': isFormer
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

                # return redirect('Community:community-interface', pk=pk)
                return JsonResponse(request.POST)
            else:
                community = Community.objects.get(id=pk)
                this_user = request.user
                this_community_user = UserCommunity.objects.filter(
                    user_id=this_user, community_id=community)
                print(this_user)
                is_former = True
                context = {
                    'this_c_user': this_community_user,
                    'is_former': is_former,
                    'community': community
                }
                print(community.upload_permission)
                return render(request, 'Community/community_setting.html', context)

# metadata: usercommunityID,  mentor_id
# vd: request.POST.usercommunityID
# method: POST
# trả về json (không render trang html)
# 1. kiểm tra trong bảng request_mentor đã có bản ghi nào trùng usercommunityID và mentor id hay chưa
# nếu có ròi thì gán cờ là flase,
# nếu chưa có thì thêm vào bảng request_mentor một bảng ghi (usercommunityID, mentorID, status = 0), gán gờ là True
# trả về json
# Khang


def request_mentor(request):
    if not request.user.is_authenticated:
        return redirect('Member:signin')
    else:
        # Retrieve usercommunityID and mentorID from POST data
        # tên của trường usercommunityid trong form
        usercommunityID = request.GET.get('user_communityID')
        # tên của trường mentorID trong form
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

# meta data: usercommunityID,  mentor_id, option
# method: POST
# 0. kiểm tra this.usercommunityID có bằng  mentor_id hay ko, ko thì return false
# 1. kiểm tra trong bảng request_mentor đã có bản ghi nào trùng usercommunityID và mentor id hay chưa
# nếu cưa có thì gán cờ là flase,
# nếu có rồi thì thay đổi status thành 1/2 phụ thuộc theo option True, False
# Khang


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


# upload document , gọi API của nhóm Hưng
def upload_document(request):
    pass


# get document and return render html
# Trung - Việt
def get_community_docments(request, pk):
    if not request.user.is_authenticated:
        return redirect('Member:signin')
    else:
        this_user = request.user
        community = Community.objects.get(id=pk)
        isMember = Validate_member(this_user, community)
        isFormer = Validate_former(this_user, community)
        if not isMember:
            redirect('Community:community-detail', pk=pk)
        else:
            community_docs = CommunityDoc.objects.filter(
                community_id=community).all()
            this_community_user = UserCommunity.objects.get(
                user_id=this_user, community_id=community)

            context = {
                'community': community,
                'this_c_user': this_community_user,
                'community_docs': community_docs,
                'is_former': isFormer
            }
            return render(request, 'Community/community_document.html', context)


def get_community_exam(request, pk):
    if not request.user.is_authenticated:
        return redirect('Member:signin')
    else:
        this_user = request.user
        EXAM_URL = "http://127.0.0.1:5000/sign_up"
        this_community_user = UserCommunity.objects.get(
            user_id=this_user, community_id=pk)
        return redirect(EXAM_URL+"?username="+this_user.username+"&score="+str(this_community_user.score))
    #     community = Community.objects.get(id=pk)
    #     isMember = Validate_member(this_user, community)
    #     isFormer = Validate_former(this_user, community)
    #     this_community_user = UserCommunity.objects.get(
    #         user_id=this_user, community_id=community)
    #     # print(Exam)

    #     if not isMember:
    #         return redirect('Community:home')
    #     else:
    #         exams = Exam.objects.filter(
    #             community_id=pk, user_id=this_user).all()
    #         context = {
    #             'exams': exams,
    #             'is_former': isFormer,
    #             'community': community,
    #             'this_c_user': this_community_user,
    #         }
    #         # for exam in exams:
    #         #     print(f"Exam ID: {exam.id}")
    #         #     print(f"Name: {exam.user.username}")
    #         #     print(f"Created Date: {exam.created_date}")
    #         # print(exams)
    # return render(request, 'Community/community_exam.html', context)


def done_exam(request):
    username = request.GET.get('username')
    score = request.GET.get('score')
    community_id = request.GET.get('community')

    # Check if the user is already logged in. If not, log them in.
    if not request.user.is_authenticated:
        # You might need to specify the user's password here.
        user = authenticate(request, username=username, password=username)
        if user is not None:
            login(request, user)
        else:
            return HttpResponse("Login failed")

    # Update the user's score in the community.
    try:
        user_community = UserCommunity.objects.get(
            user_id=request.user, community_id=community_id)
        user_community.score = int(score)
        user_community.save()
    except UserCommunity.DoesNotExist:
        return HttpResponse("User not found in the specified community")

    # Redirect the user to the community interface or any other page.
    return redirect('Community:community-interface', pk=community_id)


def back_community(request):
    username = request.GET.get('username')
    community_id = 1
    score = request.GET.get('score')
    # Check if the user is already logged in. If not, log them in.
    # if not request.user.is_authenticated:
     # You might need to specify the user's password here.
    user = authenticate(request, username=username, password=username)
    if user is not None:

            login(request, user)
    else:
            return HttpResponse("Login failed")

    if score is not None:
        try:
            user_community = UserCommunity.objects.get(
                user_id=request.user, community_id=community_id)
            user_community.score = int(score)
            user_community.save()
        except UserCommunity.DoesNotExist:
            return HttpResponse("User not found in the specified community")
    # Update the user's score in the community.

    return redirect('Community:community-interface', pk=community_id)


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
            community.Member.add(user)
            community.save()
            user_community = UserCommunity()
            user_community.user_id = user
            user_community.community_id = community
            # user_community.score=10
            user_community.save()
            return redirect('Community:community-detail', pk=pk)


def verify_exam(request):
    communityId = request.POST.get('communityId')
    userId = request.POST.get('userId')
    playerScore = request.POST.get('playerScore')
    community = Community.objects.get(id=communityId)
    user = User.objects.get(id=userId)
    err_mes = ""
    if user == None or community == None:
        flag = False
        err_mes = "user id or commmunity id not valid"
    else:
        playScore = int(request.POST.get('playerScore'))
        print(playScore)
        if playScore >= 4:
            community.Member.add(user)
            community.save()
            user_community = UserCommunity()
            user_community.user_id = user
            user_community.community_id = community
            user_community.score = 10
            user_community.save()
            flag = True

        else:
            flag = False
            err_mes = "not passed exam"
    res = {
        'flag': flag,
        'err_mess': err_mes
    }
    return JsonResponse(res)


def synchronize_data(request):
    api_url = "http://127.0.0.1:5000/get_all_users"
    response = requests.get(api_url)
    if response.status_code == 200:
        # Parse and process the data received from the API
        data = response.json()

        # Save the data to your Django models or perform other actions
        for item in data:
            if 'username' not in item:
                continue
            username = item['username']
            community_id = 1
            # Get the score from the API, default to 10
            score = int(item.get('score', 10))

            # Get or create a user with the specified username
            user, created = User.objects.get_or_create(username=username)

            if created:
                # Set the password if the user is created
                user.set_password(username)
                user.save()
            # Check if the user already has a UserCommunity record for the community

            community = Community.objects.get(id=community_id)
            user_community, created = UserCommunity.objects.get_or_create(
                user_id=user,
                community_id=community,
                # Set the score if the record is created
                defaults={'score': score}
            )

            # If the record is not created (user already had a record for the community), update the score
            if not created:
                user_community.score = score
                user_community.save()

        return JsonResponse({'message': 'Data synchronized successfully'})
    else:
        return JsonResponse({'message': 'Failed to synchronize data'}, status=500)
