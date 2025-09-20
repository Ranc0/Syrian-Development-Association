from django.shortcuts import render

from rest_framework import generics, permissions, status, viewsets
from rest_framework.decorators import action

from ..models import *
from ..serializers import *

class NewsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = News.objects.all().order_by('-created_at')
    permission_classes = [permissions.AllowAny]

    def get_serializer_class(self):
        return NewsListSerializer if self.action == 'list' else NewsDetailSerializer