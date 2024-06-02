import logging
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from .serializers import  UserSerializer, FriendRequestSerializer
from django.conf import settings
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from .filters import UserFilter
from rest_framework.validators import ValidationError
from datetime import datetime, timedelta
from django.db.models import Q
from django.db import IntegrityError
from django.shortcuts import get_object_or_404

# Create your views here.
logger = logging.getLogger(__name__)


class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]


class UserLoginView(APIView):
    def post(self, request):
        user = authenticate(username=request.data['email'], password=request.data['password'])
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        else:
            return Response({'error': 'Invalid credentials'}, status=401)
        

class UsersListAPIView(generics.ListAPIView):
    queryset = get_user_model().objects.all().order_by('id') 
    serializer_class = UserSerializer
    filterset_class = UserFilter
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter] 
    ordering_fields = ['id', 'email', 'first_name', 'last_name'] 
    ordering = ['id'] 


class PendingFriendRequestListAPIView(generics.ListAPIView):
    
    serializer_class = FriendRequestSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = self.serializer_class.Meta.model.objects.filter(status=1, sent_from=self.request.user).order_by('id') 
        return queryset

class FriendListAPIView(generics.ListAPIView):
    
    serializer_class = FriendRequestSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = self.serializer_class.Meta.model.objects.filter(status=2, sent_from=self.request.user).order_by('id') 
        return queryset
    

class SendFriendRequestAPIView(generics.CreateAPIView):
    serializer_class = FriendRequestSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        last_minutes_ago = datetime.now() - timedelta(minutes=1)
        last_minutes_fr_count = self.serializer_class.Meta.model.objects.filter(
            Q(sent_on__lte=last_minutes_ago) and Q(sent_from=self.request.user)
        ).count()
        
        if last_minutes_fr_count >= 3:
            raise ValidationError({'error': 'You cannot send more than 3 requests in one minute'})
        
        sent_to = serializer.validated_data.get('sent_to')
        sent_from = self.request.user
        
        if sent_to == sent_from:
            raise ValidationError({'error': 'User cannot send a request to itself'})
        
        try:
            serializer.save()
        except IntegrityError as e:
            raise ValidationError({'error': 'You already sent friend request to this user'})
        except Exception as e:
            raise ValidationError({'error': e})
            

class AcceptFriendRequestAPIView(generics.UpdateAPIView):
    serializer_class = FriendRequestSerializer
    permission_classes = [IsAuthenticated]
    allowed_methods=['patch']
    lookup_field = 'pk'  
    
    def perform_update(self, serializer):
        serializer.validated_data['status'] = 2
        
        serializer.save()

    def get_queryset(self):
        return self.serializer_class.Meta.model.objects.filter(sent_from=self.request.user)


class RejectFriendRequestAPIView(generics.UpdateAPIView):
    serializer_class = FriendRequestSerializer
    permission_classes = [IsAuthenticated]
    allowed_methods=['patch']
    lookup_field = 'pk'  
    
    def perform_update(self, serializer):
        serializer.validated_data['status'] = 3
        
        serializer.save()

    def get_queryset(self):
        return self.serializer_class.Meta.model.objects.filter(sent_from=self.request.user)