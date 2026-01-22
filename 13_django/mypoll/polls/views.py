

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse    # url conf의 설정 이름으로 url을 조회하는 함수 

## path("url", view함수, name="name")
# reverse("name") => url 
from django.db import transaction   # DB Transaction 처리 
from django.core.paginator import Paginator

from datetime import datetime
from .models import Question, Choice

# 설문 welcome page view
# 요청 - 인사말 화면을 응답. 
def welcome (request):     # 최소 한 개 파라미터는 선언해야 함
    print("Welcome 실행")
    # 요청 처리
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # 응답 화면 생성 -> template 호출 (template이 사용할 값을 전달)
    response = render(  # template 호출 -결과-> HttpResponse로 반환
        request,  # HttpRequest
        "polls/welcome.html",  # 호출할 template의 경로 
        {"now":now}  # template에 전달할 값들. name-value 로 전달. Context Value 라고 한다. 
    )
    print(type(response))  # server를 실행한 터미널에 출력
    return response


def welcome_old(request):
    print("welcome 실행")
    # 요청 처리
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # 처리 결과 페이지 생성 -> html을 str로 구현
    res_html = f"""<!DOCTYPE HTML>
<html>
    <head>
        <title>설문</title>
    </head>
    <body>
        <h1>Welcome</h1>
        <p>저희 설문 페이지를 방문해주셔서 감사합니다.</p>
        현재 시간: {now}
    </body>
</html>
"""
    res = HttpResponse(res_html)
    return res


# 설문 (질문) 목록 조회 
## 전체 question들을 조회해 목록 html을 반환 
## 요청 url: polls/list
## view함수: list
## template: polls/list.html 
################################################################
def list_old(request):
    # 1. DB에서 질문 목록 조회 conn -> cursor -> sql 실행 -> Model 사용 
    question_list = Question.objects.all().order_by("-pub_date")
    # 2. 응답 페이지 생성(template 사용) -> 반환
    return render(
        request, 
        "polls/list.html", 
        {"question_list":question_list}      
    )

################################################################
# Paging 처리 list

# - template 호출 전달할 Context Value
#    - 현재 페이지의 데이터 - Page 객체
#    - 현재 페이지가 속한 페이지 그룹의 페이지 번호 start/end index
#    - 현재 페이지 그룹의 시작 페이지 이전 페이지가 있는지 여부, 있다면 이전 페이지 번호
#    - 현재 페이지 그룹의 끝 페이지 다음 페이지가 있는지 여부, 있다면 다음 페이지 번호
def list(request):
    paginate_by = 10       # 한 페이지 당 데이터 개수
    page_group_count = 10  # 페이지 그룹 당 페이지 수 
    # http://ip:port/polls/list?page=6
    current_page = int(request.GET.get("page", 1))  # 현재 조회 요청이 들어온 페이지 번호. get 방식의 요청파라미터.
    # 혹시 page값 넘어온 게 없으면 default = 1을 줘 라는 뜻으로 1.

    # Paginator
    q_list = Question.objects.all().order_by("-pk") 
    pn = Paginator(q_list, paginate_by)

    # 현재 페이지가 속한 PageGroup의 시작 index, 종료 페이지의 index
    start_index = int((current_page -1) / page_group_count) * page_group_count
    end_index = start_index + page_group_count

    page_range = pn.page_range[start_index:end_index] # 시작 ~ 끝 페이지 번호 조회

    # template에 전달할 context value dictionary
    context_value = {
        "page_range" : page_range,
        "question_list" : pn.page(current_page)   # page 객체 안에 [Question]
    }

    # PageGroup의 시작 페이지가 이전 페이지가 있는지 여부, 이전 페이지 번호
    # PageGroup의 마지막 페이지가 다음 페이지가 있는지 여부, 다음 페이지 번호
    start_page = pn.page(page_range[0])  # 시작 페이지 Page 객체
    end_page = pn.page(page_range[-1])   # 마지막 페이지 Page 객체

    if start_page.has_previous():
        context_value['has_previous'] =  start_page.has_previous()
        context_value["previous_page_number"] = start_page.previous_page_number()

    if end_page.has_next():
        context_value['has_next'] = end_page.has_next()
        context_value['next_page_number'] = end_page.next_page_number()

    # 응답 template 호출
    return render(request, "polls/list.html", context_value)



# 개별 설문을 할 수 있는 페이지(설문 폼)로 이동 
## 질문 ID를 path parameter로 받아서
##     그 질문과 보기를 DB에서 조회해서 화면에 출력 - 설문 입력 폼
### path parameter: http://ip:port/path1/path2/path3/전달값1/전달값2
### request(요청) parameter: http://ip:port/path1/path2/path3?=name=전달값1&name=전달값2

# 요청 URL: /polls/vote_form/질문ID
# View함수: vote_form
# template: 정상 - polls/vote_form.html
#           오류 - polls/error.html

def vote_form(request, question_id):                                                                                                                                                                                                                                                                     
    # question_id 파라미터 - path parameter 값을 받을 변수
    # view함수의 두 번째 파라미터부터는 path parameter를 받을 변수들
    ## 파라미터 변수명은 urls.py에 등록한 변수명으로 선언하면 된다.

    # 1. DB에서 question_id로 질문을 조회
    try:
        question = Question.objects.get(pk=question_id)
        # 응답 화면 요청
        return render(
            request, 
            "polls/vote_form.html",
            {"question":question}   # context_value
        )
    except:
        # print(f"{question_id}의 질문이 없습니다.")
        return render(
            request,
            "polls/error.html",
            {"error_message":f"요청하신 {question_id}번 질문이 없습니다."}
        )


# 설문 처리하기  
## 선택한 보기(Choice)의 votes를 1 증가. 투표 결과를 보여주는 페이지로 이동. 

# 요청 URL: polls/vote
# view함수: vote
# 응답: 정상 - polls/vote_result.html
#      오류 - polls/vote_form.html

# form 입력은 요청 파라미터로 읽는다.
# 요청 파라미터: GET - request.GET -> dictionary {"요청 파라미터 이름":"요청 파라미터 값"}
#             POST - request.POST -> dictionary 

def vote(request): 
    # 요청 파라미터 조회
    choice_id = request.POST.get('choice')  # 선택된 보기의 ID
    question_id = request.POST.get('question_id')  # 질문 ID (이따 결과에서 사용할 것)

    # choice_id가 넘어왔다면 choice의 votes를 1 증가
    if choice_id != None:
        selected_choice = Choice.objects.get(pk=choice_id)
        selected_choice.votes += 1
        selected_choice.save()   # update

        # TODO 업데이트 결과를 보여주는 View(vote_result)를 redirect 방식으로 요청 
        # urls.py에 path에 등록된 이름으로 url을 조회
        ## app_name: 설정 이름
        ## path parameter 있는 경우 args=[path parameter 값, ..]
        url = reverse("polls:vote_result", args=[question_id])
        print(type(url), url)
        return redirect(url)

        # # 결과 페이지 - question 조회
        # question = Question.objects.get(pk=question_id)
        # return render(
        #     request, "polls/vote_result.html", {"question":question}
        # )

    else:  # choice를 선택하지 않고 요청한 경우.
        question = Question.objects.get(pk=question_id)
        return render(
            request,
            "polls/vote_form.html",
            {"question":question, "error_message":"보기를 선택하세요"}
        )


# 개별 질문의 투표 결과를 보여주는 View
# 요청 URL: /polls/vote_result/<question_id>
# View 함수: vote_result
# 응답: polls/vote_result.html
def vote_result(request, question_id):
    question = Question.objects.get(pk=question_id)
    return render(
        request, "polls/vote_result.html", {"question":question}
    )


# 설문 (질문)을 등록 처리
# 요청 URL: /polls/vote_create
# view함수: vote_create
#        - HTTP 요청 방식에 따라 입력 양식을 제공할 지 처리할 지 결정. 
#        - GET: 입력 양식을 제공 (설문 문제와 보기를 입력할 수 있는 화면)
#        - POST: 등록처리 
# 응답: - GET 처리: (template) polls/vote_create.html
#      - POST 처리: redirect 방식 응답 ==> list View를 요청 
# Http 요청 방식 조회 - request.method (str: "GET", "POST")

def vote_create_old(request):
    http_method = request.method
    if http_method == "GET":
        # 입력 폼 제공
        return render(request, "polls/vote_create.html")

    elif http_method == "POST":
        # 등록 처리 
        # 1. 요청 (path) 파라미터 읽기
        # 2. 요청 파라미터 검증 (조건 안 맞거나, 숫자여야 하는데 문자열 들어왔거나, 개수 안 맞거나 등) -성공-> 처리, 실패-> 입력 폼 페이지(error)를 응답
        # 3. 업무 처리 -> DB 작업
        # 4. 응답
        
        # 요청 파라미터 조회 - POST 방식일 땐 post, get방식 일 땐 get : request.POST(GET) => dictionary구현체
        ## 요청 파라미터 중 question_text를 조회
        question_text = request.POST.get("question_text")
        ### 요청 파라미터 중 choice_text를 조회 (같은 이름으로 여러 개 전달)
        #### choice_text=보기1&choice_text=보기2& ...   # choice_text가 같은 이름으로 여러 개 넘어오면 get으로 읽어야 함.
        choice_list = request.POST.getlist("choice_text")  # list[str]

        # 요청 파라미터 검증 (질문: 1글자 이상, 보기: 2개 이상 각각 1글자 이상)
        if not question_text.strip(): # 빈 문자열일 경우 
            return render(
                request, "polls/vote_create.html",
                {"error_msg":"문제를 한 글자 이상 입력하세요.", "question_text":question_text, "choice_list": choice_list}
            )
        
        ## 보기 검증. choice_text가 넘어온 게 없거나  
        ##         (choice_text가 넘어온 게 있는데 값이 있는 것이 2개가 안 되면) ==> 검증 실패
        if not choice_list or (choice_list and len([c for c in choice_list if c.strip()]) < 2):
            return render(
                request, "polls/vote_create.html",
                {"error_msg":"보기는 두 개 이상 입력해야 합니다.", "question_text":question_text, "choice_list": choice_list}
            )
        try:
            # with block을 정상적으로 처리하면 commit 실행. 
            # with block 실행 중 Exception이 발생하면 rollback (Insert 작업 처음 상태로 돌린다.) 
            
            with transaction.atomic():  # Transaction 시작
                # 검증 통과 -> DB에 저장 (Insert)
                # 모델 객체.save()
                q = Question(question_text=question_text)  # id/pub_date 자동 입력.
                q.save() 

                # raise Exception("문제가 발생했습니다.")

                for c in choice_list:
                    choice = Choice(choice_text=c, question=q) # id/vote 는 자동 입력되게 생략. default=0으로 셋팅.
                    choice.save()

        except Exception as e:
            # error page로 이동
            return render(request, #"polls/error.html", 
                          "error.html",  # 공통 error page
                          {"error_message":f"질문을 저장하는 도중 문제가 발생했습니다. 관리자에게 문의하세요."})

        # 4. 응답- list로 redirect 방식으로 이동
        return redirect(reverse("polls:list"))


from .forms import QuestionForm, ChoiceFormSet


# forms.py의 Form을 이용한 요청 파라미터 처리 view 함수
@login_required  # @ : decorator는 사용환경한테 보여주는 것. 이 함수 실행 전에 로그인이 필요하다는 뜻. 
def vote_create(request):
 
    if request.method == "GET":
        # 등록 폼 페이지 반환
        ## 등록 폼 -> forms.QuestionForm 를 이용 
        q_form = QuestionForm()   # 질문
        c_formset = ChoiceFormSet() # 보기들
        # <input type=text> X extra 개수 => 이름(index로 관리)
        #      prefix - index번호 - field이름 (form-0-choice_text)

        return render(
            request, "polls/vote_create_form.html", {"q_form":q_form, "c_formset":c_formset}
        )

    elif request.method == "POST":
        # 등록 처리
        # 요청 파라미터 조회+검증 -> Form을 이용해서 조회/검증
        # 요청 파라미터 조회해서 검증을 통과하면 Form객체에 넣는다.
        # 요청 파라미터값들은 form의 dictionary로 관리되고 cleaned_data 속성으로 조회 가능. 
        q_form = QuestionForm(request.POST) # 요청 파라미터의 값을 속성으로 가지는 Form
        c_formset = ChoiceFormSet(request.POST) #, prefix='choice') 생성할 때 prefix를 지정했으면 여기서도 지정해줘야 함. 
        # print("---------------", q_form)
        # print("---------------", c_formset)

        # 검증을 통과했는지 여부 - form.is_valid(): bool (True - 통과, False - 검증실패)
        if q_form.is_valid() and c_formset.is_valid():  # 요청파라미터 검증에 문제 없으면
            # 요청파라미터 읽어서 조회. form객체. cleaned_data: dict
            question_text = q_form.cleaned_data['question_text'] # key: Field 이름
            choice_list = []
            for c_form in c_formset:
                choice_list.append(c_form.cleaned_data["choice_text"])

            # DB 저장
            try:
                with transaction.atomic():
                    q = Question(question_text=question_text)
                    q.save()

                    for choice_text in choice_list:
                        c = Choice(choice_text=choice_text, question=q)
                        c.save()

            except:
                return render(request, "error.html", {"error_message":"질문/보기 DB 저장 도중 문제 발생"})

            return redirect(reverse("polls:list"))

        else:  # 요청파라미터 검증 실패 => Form객체는 ValidationError객체를 가지고 있다. 
               # 에러 처리 페이지로 이동 --> 등록페이지로 이동
            return render(
                request, "polls/vote_create_form.html",
                {"q_form":q_form, "c_formset":c_formset} # validation(검증) 실패한 form들을 context_value로 전달.
            )


# 설문 질문 삭제 처리
# 요청 URL: /polls/vote_delete/삭제할 질문_PK
# view 함수: vote_delete
# 응답     : redirect - polls:list
def vote_delete(requst, question_id):
    # 삭제할 데이터 조회
    question = Question.objects.get(pk=question_id)
    # 삭제
    question.delete()
    