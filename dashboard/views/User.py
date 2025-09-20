from rest_framework import generics, permissions
from django.contrib.auth import get_user_model
from dashboard.serializers import *

User = get_user_model()
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

class IsDashboardUser:
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_type in ['admin', 'staff']


class UserListDashboardView(generics.ListAPIView):
    serializer_class = DashboardUserListSerializer
    permission_classes = [permissions.IsAuthenticated , IsDashboardUser]

    def get_queryset(self):
        user = self.request.user
        if user.user_type != 'admin':
            raise PermissionDenied("You do not have permission to view this resource.")
        return User.objects.filter(user_type__in=['admin', 'staff'])

class BeneficiaryUserListDashboardView(generics.ListAPIView):
    serializer_class = DashboardUserListSerializer
    permission_classes = [permissions.IsAuthenticated , IsDashboardUser]

    def get_queryset(self):
        user = self.request.user
        if user.user_type != 'admin' and user.user_type != 'staff':
            raise PermissionDenied("You do not have permission to view this resource.")
        return User.objects.filter(user_type__in=['beneficiary'])

from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied
from dashboard.serializers import UserCreateSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class DashboardUserCreateView(generics.CreateAPIView):
    serializer_class = UserCreateSerializer
    permission_classes = [permissions.IsAuthenticated, IsDashboardUser]

    def perform_create(self, serializer):
        user = self.request.user
        if user.user_type != 'admin':
            raise PermissionDenied("Only admins can create new users.")
        serializer.save()

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from dashboard.serializers import EmailLoginSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.generics import GenericAPIView

class SignInView(GenericAPIView):
    serializer_class = EmailLoginSerializer
    permission_classes=[]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)

from rest_framework.exceptions import PermissionDenied, NotFound

class DeleteUserByIdView(APIView):
    permission_classes = [permissions.IsAuthenticated , IsDashboardUser]

    def delete(self, request, user_id):
        if request.user.user_type != 'admin':
            raise PermissionDenied("Only admins are allowed to delete users.")

        try:
            user_to_delete = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            raise NotFound("User not found.")

        user_to_delete.delete()
        return Response({"detail": "User deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

class DashboardForgotPasswordView(APIView):
    permission_classes = []

    def post(self,request):
        serializer=DashboardForgotPasswordSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"تم ارسال رمز التحقق "},status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class DashboardVerifyOTPView(APIView):
    permission_classes = []

    def post(self,request):
        serializer=DashboardConfirmOTPSerializer(data=request.data)
        if serializer.is_valid():
            return Response({"message":"تم التحقق بنجاح"},status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class DashboardResetPasswordView(APIView):
    permission_classes = []

    def post(self,request):
        serializer=DashboardResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"تم تغيير كلمة المرور بنجاح"},status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    permission_classes=[IsAuthenticated , IsDashboardUser]
    def post(self,request):
        serializer=LogoutSerializer(data=request.data , context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message":"تم تسجيل الخروج بنجاح"},status=status.HTTP_205_RESET_CONTENT)
