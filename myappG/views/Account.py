from django.shortcuts import render

from rest_framework import generics, permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, FormParser
from django.contrib.auth import authenticate
from ..models import PendingUser ,CustomUser
from ..serializers import *

class RegisterPendingUserView(APIView):
    permission_classes=[]
    def post(self, request):
        serializer = RegisterPendingUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "تم ارسال رمز التحقق إلى بريدك الإلكتروني"}, status=status.HTTP_200_OK)

class ConfirmOTPView(APIView):
    permission_classes=[]

    def post(self, request):
        serializer = ConfirmOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "تم تأكيد الرمز وإنشاء الحساب بنجاح"}, status=status.HTTP_201_CREATED)

class LoginView(generics.GenericAPIView):
    serializer_class = EmailLoginSerializer
    permission_classes=[]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)

class ProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = ProfileUserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UpdateUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request):
        serializer = ProfileUserSerializer(
            request.user, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

class ForgotPasswordRequestView(APIView):
    permission_classes = []

    def post(self, request):
        serializer = ForgotPasswordRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            "message": "تم ارسال رمز التحقق إلى بريدك الإلكتروني",
            "otp": serializer.data.get("otp")
        }, status=status.HTTP_200_OK)

class ConfirmPasswordResetOTPView(APIView):
    permission_classes = []

    def post(self, request):
        serializer = ConfirmPasswordResetOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({"message": "تم التحقق من الرمز بنجاح، يمكنك الآن تعيين كلمة سر جديدة"}, status=status.HTTP_200_OK)


class ResetPasswordView(APIView):
    permission_classes = []
    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "تم تعيين كلمة السر الجديدة بنجاح"}, status=status.HTTP_200_OK)

class LogoutView(APIView):
    permission_classes=[permissions.IsAuthenticated]
    def post(self,request):
        serializer=LogoutSerializer(data=request.data , context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message":"تم تسجيل الخروج بنجاح"},status=status.HTTP_205_RESET_CONTENT)
