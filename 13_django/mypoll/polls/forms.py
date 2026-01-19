from django import forms

# form class를 정의 - forms.Form을 상속받아 만든다.
## form class: 입력 폼들을 모아서 정의한 클래스 
##           - Form Field: 개별 입력 폼(input)들을 정의 
##                          class 변수로 정의. 입력 폼 양식 - python type 관련되어 FormField 객체를 할당. 

# 설문 질문 등록 폼 
class QuestionForm(forms.Form):
    # Form Field -> 질문 입력
    # 변수명 (요청 파라미터 name) = FormField(): 어떤 값을 입력받을지 타입.

    # Form Field 1개 -> 한 개 이름의 요청파라미터 입력 태그를 설정. 
    ## 같은 이름으로 여러 개 입력을 받을 경우 -> Form set을 이용해서 구현 
    question_text = forms.CharField( # 문자열 입력 폼 - View에서 문자열로 읽기.
        label="질문",  # 입력에 대한 label을 설정. 
        max_length=200, # 최대 입력 글자 수
        required=True, # 필수 입력인지 여부
        widget=forms.TextInput( # widget은 input 태그를 지정.
            attrs={"class":"form-control"}   # 입력 tag의 attribute 설정. 
        )
    )

    choice_text = forms.CharField(
        label="보기",
        max_length=200,
        required=True
    )