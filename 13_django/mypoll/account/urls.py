from django.urls import path
from . import views

app_name = "account"

urlpatterns =[  # 이게 없으면 이 파일을 url 파일이라고 인식하지 못함. 
    # http://127.0.0.1
    path("create", views.create, name="create"),
    path("detail/<str:user_id>", views.detail, name="detail"),
]