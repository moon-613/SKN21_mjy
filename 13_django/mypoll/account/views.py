from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import (
    authenticate, # 인증 확인: username, password를 DB에서 확인
    login,  # login 처리 - 로그인한 사용자 정보(User Model)를 session에 추가.
    logout, # 로그아웃 처리 - session에서 사용자 정보를 제거.
    update_session_auth_hash # 회원정보 수정 처리에서 사용. session의 사용자 정보를 수정한 것을 변경. 
)
from django.contrib.auth.forms import (
    AuthenticationForm, # login form
    PasswordChangeForm, # password 변경 화면의 폼
)
from .models import CustomUser 
from .forms import CustomUserChangeForm, CustomUserCreationForm
 
# 가입 처리
# 요청 URL: account/create
# View 함수: create
#      - GET: 가입 입력 페이지를 반환
#      - POST: 가입 처리
# 응답
#      - GET: templates/account/create.html
#      - POST: main으로 이동. (polls/welcome.html)

def create(request):

    if request.method == "GET":
        # 폼 객체를 context value로 전달.
        return render(
            request,
            "account/create.html",
            {"form": CustomUserCreationForm()}
        )
    
    elif request.method == "POST":
        # 가입 처리
        ## 1. 요청 파라미터 조회 및 검증
        form = CustomUserCreationForm(request.POST)

        if form.is_valid(): # 요청 파라미터에 문제가 없는 경우
            ## 2. DB에 저장
            # ModelForm은 save()를 제공. 요청 파라미터 값들을 DB에 insert/update 해준다. 
            user = form.save()  # 반환: save() 처리한 Model 객체를 반환. 
            print(type(user), user)

            ## 3. 응답
            return redirect(reverse("polls:welcome"))

        else: # 요청파라미터에 문제가 있는 경우.
            return render(
                request,
                "account/create.html",
                {"form": form}  # 문제가 있는 Form을 context value로 전달. 
            )
        
# 가입한 사용자 정보 조회
# URL: /account/detail/<user_id> (TODO: user_id는 나중에 로그인 처리 후 변경)
# 함수: detail
# 응답: account/detail.html

def detail(request, user_id):
    try:
        user = CustomUser.objects.get(username=user_id)
        return render(
            request, "account/detail.html", {"user":user}
        )

    except:
        return render(request, "error.html", {"error_message":"회원정보 조회 도중 문제 발생"})
    
# 로그인 처리 구현
# 요청 URL: /account/login
# 함수: user_login
#    - GET: 로그인 폼 페이지로 이동. (account/login.html)
#    - POST: 로그인 처리 (redirect- polls:welcome)
def user_login(request):
    if request.method == "GET":
        return render(
            request,
            "account/login.html",
            {"form":AuthenticationForm()}
        )

    elif request.method == "POST":
        pass