# config/urls.py -> URL Conf(Url Dispatcher, URL Mapping)
# url과 view를 연결. 어떤 url로 요청이 들어오면 어떤 view가 실행될지를 연결 및 설정
"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
# from polls.views import welcome
urlpatterns = [
    path('admin/', admin.site.urls),
    path("polls/", include("polls.urls")),  # polls/로 시작하는 url 경로로 요청이 들어오면 polls 앱 밑에 urls.py의 설정을 가서 나머지를 확인. 
    # path('polls/welcome', welcome, name="poll_welcome"),  # 1. client 요청 경로, 2. 호출할 view 함수 지정, 3. name="설정 이름" 
    path("account/", include("account.urls")),
]
# 요청경로: 'polls/welcome/ -> "http://IP:port/    polls/welcome"

