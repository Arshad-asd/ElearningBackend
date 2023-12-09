from django.shortcuts import render
from rest_framework.response import Response

from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.generics import UpdateAPIView,RetrieveAPIView

from rest_framework import status
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication
from rest_framework.permissions import IsAuthenticated,BasePermission,AllowAny
from .serializers import  TutorRegistrationSerializer, UserProfileSerializer, UserRegistrationSerializer 
from .serializers import CustomTokenObtainPairSerializer, CustomTokenRefreshSerializer,UserSerializer

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView ,TokenRefreshView
# Create your views here.
from django.db.models import Q

from .models import UserAccount


class GetRoutesView(APIView):
    def get(self, request):
        routes = [
            'api/token/user',
            'api/token/admin',
            'api/token/refresh/',
            'api/token/verify/',
            'api/user/register',
            'api/tutor/register/'
        ]

        return Response(routes)

#<--------------------------------------------------------User_Side-Start------------------------------------------------------------>

class UserRegistrationView(APIView):

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            return Response(UserRegistrationSerializer(user).data, status=status.HTTP_201_CREATED)
        


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class CustomTokenRefreshView(TokenRefreshView):
    serializer_class = CustomTokenRefreshSerializer


class UserProfileView(RetrieveAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        return self.request.user

class UserDetialiView(RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        return self.request.user

class UserProfileUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = self.request.user
        serializer = UserProfileSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        user = self.request.user
        serializer = UserProfileSerializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#<------------------------------------------------------Admin-Side-Start------------------------------------------------------------------>

class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == 'admin'

class LogoutView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request, *args, **kwargs):

        request.auth.delete()
        return Response({'detail': 'Logout successful'}, status=status.HTTP_200_OK)


class UserListView(generics.ListAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        # Filter users by the 'student' role
        queryset = UserAccount.objects.filter(role='student')

        # Get the search term from the query parameters
        search_term = self.request.query_params.get('search', None)

        # If search term is provided, filter the queryset based on it
        if search_term:
            queryset = queryset.filter(
                Q(id__icontains=search_term) |
                Q(first_name__icontains=search_term) |
                Q(last_name__icontains=search_term) |
                Q(email__icontains=search_term)
            )

        return queryset

class BlockUnblockUserView(UpdateAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        return UserAccount.objects.all()

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance:
            instance.is_active = not instance.is_active
            instance.save()

            serializer = self.get_serializer(instance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)


class TutorListView(generics.ListAPIView):

    serializer_class = UserSerializer
    def get_queryset(self):
        # Filter users by the 'student' role
        return UserAccount.objects.filter(role='tutor')


#<------------------------------------------------------Tutor-Side-Start----------------------------------------------------------------->
class TutorRegistrationView(APIView):

    def post(self, request):
        serializer = TutorRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            return Response({"message": "Tutor registration successful"}, status=status.HTTP_201_CREATED)
