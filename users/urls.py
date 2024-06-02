from django.urls import path
from .views import SignupView, LoginView, UserSearchView, SendFriendRequestView, ManageFriendRequestView, ListFriendsView, ListPendingFriendRequestsView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('users/search/', UserSearchView.as_view(), name='user_search'),
    path('friend-requests/send/', SendFriendRequestView.as_view(), name='send_friend_request'),
    path('friend-requests/manage/<int:pk>/', ManageFriendRequestView.as_view(), name='manage_friend_request'),
    path('friends/', ListFriendsView.as_view(), name='list_friends'),
    path('friend-requests/pending/', ListPendingFriendRequestsView.as_view(), name='list_pending_friend_requests'),
]
