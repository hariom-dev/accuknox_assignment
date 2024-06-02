from rest_framework import serializers
from .models import CustomUser, FriendsRequest

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class FriendRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendsRequest
        fields = ['id', 'sent_from', 'sent_to', 'status']
        extra_kwargs = {
            'id': {'read_only': True},
            'sent_from': {'read_only': True}, 
            'sent_from': {'read_only': True}
        }
        
    def create(self, validated_data):
        
        validated_data['sent_from'] = self.context['request'].user
        return super().create(validated_data)
