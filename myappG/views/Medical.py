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
from django.core.exceptions import PermissionDenied
from rest_framework.exceptions import NotFound , ValidationError

class MedicalAidRequestViewSet(viewsets.ModelViewSet):
    serializer_class = MedicalAidRequestSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        return MedicalAidRequest.objects.none()

    def list(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def get_object(self):
        user = self.request.user

        if user.user_type == 'beneficiary':
            try:
                beneficiary = Beneficiary.objects.get(user=user)
                return MedicalAidRequest.objects.get(beneficiary=beneficiary)
            except (Beneficiary.DoesNotExist, MedicalAidRequest.DoesNotExist):
                raise NotFound("No medical aid request found for this user.")
        else:
            raise PermissionDenied("Only beneficiaries are allowed to access this resource.")

    def retrieve(self, request, *args, **kwargs):
        obj = self.get_object()
        serializer = self.get_serializer(obj)
        return Response(serializer.data)

    def perform_create(self, serializer):
        user = self.request.user

        if user.user_type == 'beneficiary':
            try:
                beneficiary = Beneficiary.objects.get(user=user)
            except Beneficiary.DoesNotExist:
                raise PermissionDenied("You must be a registered beneficiary to submit this request.")

            if MedicalAidRequest.objects.filter(beneficiary=beneficiary).exists():
                raise ValidationError("You already have a medical aid request.")
            
            serializer.save(beneficiary=beneficiary)
        else:
            serializer.save()


    def update(self, request, *args, **kwargs):
        raise PermissionDenied("Updating medical aid requests is not allowed.")

    def partial_update(self, request, *args, **kwargs):
        raise PermissionDenied("Updating medical aid requests is not allowed.")

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.status != 'pending':
            raise PermissionDenied("Only pending requests can be deleted.")
        return super().destroy(request, *args, **kwargs)