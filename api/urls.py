# api/urls.py

from django.urls import path
from .views import SignupView, LoginView, UserSearch, FriendRequestView, FriendsList, FriendRequestAction

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('search/', UserSearch.as_view(), name='search'),
    path('friend-request/', FriendRequestView.as_view(), name='friend-request'),
    path('friend-request-action/', FriendRequestAction.as_view(), name='friend-request-action'),
    path('friends/', FriendsList.as_view(), name='friends'),
]