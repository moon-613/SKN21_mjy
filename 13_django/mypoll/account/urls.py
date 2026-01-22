from django.urls import path
from . import views

app_name = "account"

urlpatterns =[  # 이게 없으면 이 파일을 url 파일이라고 인식하지 못함. 
    # http://127.0.0.1
    path("create", views.create, name="create"),
    path("detail", views.detail, name="detail"),
    path("login", views.user_login, name="login"),
    path("logout", views.user_logout, name="logout"),
    path("update", views.update, name="update"),
    path("password_change", views.password_change, name="password_change"),
    path("delete", views.user_delete, name="delete"),
]