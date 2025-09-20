from rest_framework import generics, permissions, status
from rest_framework.exceptions import PermissionDenied, NotFound
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils import timezone

from myappG.models import MaterialAidRequest
from dashboard.serializers import (
    MaterialAidUpdateResponseSerializer,
MaterialAidDashboardDetailSerializer,
MaterialAidDashboardSerializer)

class MaterialAidDashboardListView(generics.ListAPIView):
    serializer_class = MaterialAidDashboardSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.user_type not in ['admin', 'staff']:
            raise PermissionDenied("You do not have permission.")
        status_param = self.request.query_params.get('status')
        qs = MaterialAidRequest.objects.all()
        if status_param and status_param.lower() != 'all':
            qs = qs.filter(status=status_param.lower())
        return qs

class MaterialAidDashboardDetailView(generics.RetrieveAPIView):
    serializer_class = MaterialAidDashboardDetailSerializer
    queryset = MaterialAidRequest.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'pk'

    def get_object(self):
        if self.request.user.user_type not in ['admin', 'staff']:
            raise PermissionDenied("You do not have permission.")
        return super().get_object()

class MaterialAidReviewStatusUpdateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, pk):
        if request.user.user_type not in ['admin', 'staff']:
            raise PermissionDenied("Only admin or staff can review requests.")
        try:
            request_obj = MaterialAidRequest.objects.get(pk=pk)
        except MaterialAidRequest.DoesNotExist:
            raise NotFound("Material aid request not found.")

        new_status = request.data.get("status")
        delivery_date = request.data.get("delivery_date")

        if new_status not in ['pending', 'approved', 'rejected']:
            return Response({"error": "Invalid status."}, status=400)

        request_obj.status = new_status
        request_obj.reviewer = request.user
        request_obj.review_date = timezone.now()

        if delivery_date:
            request_obj.delivery_date = delivery_date

        request_obj.save()

        serializer = MaterialAidUpdateResponseSerializer(request_obj)
        return Response(serializer.data, status=200)