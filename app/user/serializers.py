"""
Serializers for the user API View.
数据验证:

UserSerializer首先会对传入的数据进行验证。它会检查数据是否包含email, password, 和name这三个字段
同时还会检查password字段是否满足最少5个字符的要求。
如果数据不符合要求
，序列化器会生成一个错误
并且视图会返回一个HTTP 400错误给客户端。
数据保存:

如果数据验证成功
序列化器的create方法会被调用。在这个方法中
它会使用get_user_model().objects.create_user方法来创建一个新的用户。请注意
create_user方法确保密码被正确地加密存储
，而不是明文。
用户对象被成功创建后
它会被返回给CreateUserView。


在Django Rest Framework (DRF) 中，序列化主要有以下作用：
数据验证：在数据从前端发送到后端时，序列化器验证该数据是否满足预设的条件。
例如，确保一个字段的值不为空，或者一个字符串字段的值满足最小和最大长度要求。
"""
from django.contrib.auth import (
    get_user_model,
    authenticate,
)
from django.utils.translation import gettext as _

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object."""

    class Meta:
        model = get_user_model()
        fields = ['email', 'password', 'name']
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        """Create and return a user with encrypted password."""
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Update and return user."""
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user auth token."""
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False,
    )

    def validate(self, attrs):
        """Validate and authenticate the user."""
        email = attrs.get('email')
        password = attrs.get('password')
        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password,
        )
        if not user:
            msg = _('Unable to authenticate with provided credentials.')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs