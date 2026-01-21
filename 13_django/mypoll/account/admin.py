from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


# 사용자 정의 UserAdmin 정의
## 관리자 앱에서 User의 어떤 항목 (Field)들을 관리할지 정의.
## UserAdmin을 상속해서 구현. admin.site.register()에 모델과 함께 등록.

## UserAdmin에서 정의할 것 (class 변수로 정의)
## list_display: list - 사용자 메인 화면에서 목록에 나올 항목들 정의 
## add_fieldsets: tuple - 등록 화면에 나올 항목들 지정
## fieldsets: tuple - 수정 화면에 나올 항목들 지정









admin.site.register(CustomUser)
