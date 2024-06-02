from rest_framework import generics, status, filters, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.throttling import UserRateThrottle
from .serializers import SignupSerializer, LoginSerializer, UserSerializer, FriendRequestSerializer
from .models import FriendRequest
from django.db.models import Q
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model
from rest_framework.pagination import PageNumberPagination
from rest_framework.exceptions import ValidationError

User = get_user_model()

class SignupView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = SignupSerializer
    permission_classes = [permissions.AllowAny]

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(
            email=serializer.validated_data['email'].lower(),
            password=serializer.validated_data['password']
        )
        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key})
        return Response({"error": "Invalid Credentials"}, status=status.HTTP_400_BAD_REQUEST)

class UserSearchView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['email', 'username']
    pagination_class = PageNumberPagination
    queryset = User.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(email__iexact=search) | Q(username__icontains=search)
            )
        return queryset

class SendFriendRequestView(generics.CreateAPIView):
    serializer_class = FriendRequestSerializer
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    def perform_create(self, serializer):
        serializer.save(from_user=self.request.user)

class ManageFriendRequestView(generics.UpdateAPIView):
    serializer_class = FriendRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return FriendRequest.objects.get(id=self.kwargs['pk'])

    def perform_update(self, serializer):
        status = self.request.data.get('status')
        if status in ['accepted', 'rejected']:
            serializer.save(status=status)
        else:
            raise ValidationError("Invalid status")

class ListFriendsView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        friend_requests = FriendRequest.objects.filter(
            Q(from_user=user, status='accepted') | Q(to_user=user, status='accepted')
        )
        friends = []
        for request in friend_requests:
            if request.from_user == user:
                friends.append(request.to_user)
            else:
                friends.append(request.from_user)
        return User.objects.filter(id__in=[friend.id for friend in friends])

class ListPendingFriendRequestsView(generics.ListAPIView):
    serializer_class = FriendRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return FriendRequest.objects.filter(to_user=self.request.user, status='sent')
    