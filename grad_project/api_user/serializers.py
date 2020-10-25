from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)
    class Meta:
        model = User
        fields = '__all__'
        # 모델 User의 모든 field를 serializer함.