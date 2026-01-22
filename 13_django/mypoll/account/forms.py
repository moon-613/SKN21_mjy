## ModelForm
## 기본 ModelForm: forms.ModelForm을 상속해서 정의
##              : Meta 내부 클래스에 어떤 모델의 어떤 필드를 이용해 정의할지 설정
##              : Model에 없는 것을 Form Field로 추가할 경우 class 변수로 정의 

from django import forms
# 장고에서 사용자 등록, 사용자 정보 수정 화면을 위해 제공하는 ModelForm 들.
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

# 사용자 등록 폼
class CustomUserCreationForm(UserCreationForm):

    # UserCreationForm에서 제공하는 입력 필드를 다시 재정의
    username = forms.CharField(label="ID", required=True, max_length=30)

    class Meta:
        model = CustomUser # 지정한 Model의 Field들을 이용해 Form을 구성.
        
        # 지정한 field들을 이용해서 form 구성 
        fields = ["username", "password1", "password2", "name", "email", "birthday", "profile_img"]
        # fields = "__all__"  # 모델의 모든 field들을 다 이용해서 Form을 구성
        # exclude = ["필드명"]  # 지정한 field를 제외한 나머지를 이용해서 Form 구성. field와 exclude는 같이 설정할 수 없다.

        # Field의 기본 위젯 (입력 타입)을 변경할 때 widgets에 지정한다.
        # key: field - value: form Widget 객체
        widgets = {
            "birthday":forms.DateInput(attrs={"type":"date"})
        }

    # 검증 메소드 추가 (전체: clean(), 개별 필드: clean_필드명())
    def clean_name(self):
        name = self.cleaned_data['name'] # 기본 검증 통과한 
        if len(name) < 2: # 이름은 두 글자 이상이면 통과
            raise forms.ValidationError("이름은 두 글자 이상 입력하세요.")
        return name
            
# 사용자 정보 수정 폼
class CustomUserChangeForm(UserChangeForm):
    # 패스워드 변경 메뉴는 나오지 않게 설정
    password = None

    class Meta:
        model = CustomUser
        fields = ["name", "email", "birthday"]
        widgets = {
            "birthday":forms.DateInput(attrs={"type":"date"})
        }

    def clean_name(self):
        name = self.cleaned_data['name'] # 기본 검증 통과한 
        if len(name) < 2: # 이름은 두 글자 이상이면 통과
            raise forms.ValidationError("이름은 두 글자 이상 입력하세요.")
        return name
