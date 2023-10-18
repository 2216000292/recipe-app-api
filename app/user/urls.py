"""
URL mappings for the user API.
URL 路由:
当Django接收到这个请求后
它会查找urls.py中定义的URL模式来确定应该如何处理这个请求。在app/user/urls.py中
我们看到路径create/是映射到CreateUserView的。因此
，请求会被转发给这个视图来处理。
"""
from django.urls import path

from user import views


app_name = 'user'

urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('token/', views.CreateTokenView.as_view(), name='token'),
    path('me/', views.ManageUserView.as_view(), name='me'),
]
