from django.shortcuts import render

from rest_framework import generics, permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, FormParser
from django.contrib.auth import authenticate
from ..models import *
from ..serializers import *

class FeedbackView(APIView):
    permission_classes=[permissions.IsAuthenticated]
    def post (self,request):
        serializer=FeedbackSerializer(data=request.data,context={'request':request})
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'تم ارسال التقييم بنجاح'},status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    def get(self,request):
        try:
            feedback=Feedback.objects.get(user=request.user)
            serializer=FeedbackSerializer(feedback)
            return Response(serializer.data)
        except Feedback.DoesNotExist:
            return Response({'details':'لم يتم ارسال تقييم بعد'},status=status.HTTP_404_NOT_FOUND)
        



