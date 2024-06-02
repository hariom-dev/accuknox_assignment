from django.urls import path
from .views import (UserRegistrationView, 
                    UserLoginView, 
                    UsersListAPIView, 
                    SendFriendRequestAPIView, 
                    PendingFriendRequestListAPIView,
                    AcceptFriendRequestAPIView,
                    RejectFriendRequestAPIView,
                    FriendListAPIView
                )

urlpatterns = [
    path('login/', UserLoginView.as_view()),
    path('register/', UserRegistrationView.as_view()),
    path('list/', UsersListAPIView.as_view()),
    path('friend/list/', FriendListAPIView.as_view()),
    path('friend/request/send/', SendFriendRequestAPIView.as_view()),
    path('friend/request/accept/<int:pk>/', AcceptFriendRequestAPIView.as_view()),
    path('friend/request/reject/<int:pk>/', RejectFriendRequestAPIView.as_view()),
    path('friend/request/pending/list/', PendingFriendRequestListAPIView.as_view()),
]