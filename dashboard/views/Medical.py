from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied
from dashboard.serializers import MedicalAidDashboardSerializer , MedicalAidDashboardDetailSerializer , MedicalAidUpdateResponseSerializer
from myappG.models import MedicalAidRequest

from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied
from myappG.models import MedicalAidRequest
from dashboard.serializers import MedicalAidDashboardSerializer

class MedicalAidDashboardView(generics.ListAPIView):
    serializer_class = MedicalAidDashboardSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.user_type not in ['admin', 'staff']:
            raise PermissionDenied("You do not have permission to view medical aid requests.")

        status_param = self.request.query_params.get('status')

        queryset = MedicalAidRequest.objects.all()

        if status_param and status_param.lower() != 'all':
            queryset = queryset.filter(status=status_param.lower())

        return queryset
    
class MedicalAidRequestDetailDashboardView(generics.RetrieveAPIView):
    serializer_class =  MedicalAidDashboardDetailSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = MedicalAidRequest.objects.all()
    lookup_field = 'pk'

    def get_object(self):
        user = self.request.user
        if user.user_type not in ['admin', 'staff']:
            raise PermissionDenied("You do not have permission to view this request.")
        return super().get_object()

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.exceptions import PermissionDenied, NotFound
from django.utils import timezone
from myappG.models import MedicalAidRequest
from myappG.serializers import MedicalAidRequestSerializer  # or a custom one if needed

class MedicalAidReviewStatusUpdateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, pk):
        user = request.user
        if user.user_type not in ['admin', 'staff']:
            raise PermissionDenied("Only admin or staff can review requests.")

        try:
            medical_request = MedicalAidRequest.objects.get(pk=pk)
        except MedicalAidRequest.DoesNotExist:
            raise NotFound("Medical aid request not found.")

        new_status = request.data.get("status")
        delivery_date = request.data.get("delivery_date")

        if new_status not in ['pending', 'approved', 'rejected']:
            return Response({"error": "Invalid status value."}, status=status.HTTP_400_BAD_REQUEST)

        medical_request.status = new_status
        medical_request.reviewer = user
        medical_request.review_date = timezone.now()

        if delivery_date:
            medical_request.delivery_date = delivery_date

        medical_request.save()

        serializer = MedicalAidUpdateResponseSerializer(medical_request)
        return Response(serializer.data, status=status.HTTP_200_OK)
