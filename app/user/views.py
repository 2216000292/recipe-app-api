"""
Views for the user API.
"""
from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from user.serializers import (
    UserSerializer,
    AuthTokenSerializer,
)

"""
在CreateUserView中
它知道这是一个创建用户的请求。由于它继承自generics.CreateAPIView
，这个视图已经预先知道它应该做什么：接收数据，验证数据，并创建一个新的用户。
CreateUserView会查看它的serializer_class属性来确定使用哪个序列化器。在这里
它会使用UserSerializer。

CreateUserView使用UserSerializer将新创建的用户对象序列化为JSON格式
"""
class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system."""
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user."""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user."""
    serializer_class = UserSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """Retrieve and return the authenticated user."""
        return self.request.user
