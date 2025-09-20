from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied
from myappG.models import ProjectRequest
from dashboard.serializers import (
    ProjectRequestDashboardSerializer,
    ProjectRequestDashboardDetailSerializer,
)
class ProjectRequestDashboardListView(generics.ListAPIView):
    serializer_class = ProjectRequestDashboardSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.user_type not in ['admin', 'staff']:
            raise PermissionDenied("You do not have permission.")

        queryset = ProjectRequest.objects.all()

        status_param = self.request.query_params.get('status')
        type_param = self.request.query_params.get('project_type')

        if status_param and status_param.lower() != 'all':
            queryset = queryset.filter(status=status_param.lower())

        if type_param and type_param.lower() != 'all':
            queryset = queryset.filter(project_type=type_param.lower())

        return queryset
    
class ProjectRequestDashboardDetailView(generics.RetrieveAPIView):
    serializer_class = ProjectRequestDashboardDetailSerializer
    queryset = ProjectRequest.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'pk'

    def get_object(self):
        if self.request.user.user_type not in ['admin', 'staff']:
            raise PermissionDenied("You do not have permission.")
        return super().get_object()
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.exceptions import PermissionDenied, NotFound
from django.utils import timezone
from myappG.models import ProjectRequest
from dashboard.serializers import ProjectUpdateResponseSerializer

class ProjectReviewStatusUpdateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, pk):
        user = request.user
        if user.user_type not in ['admin', 'staff']:
            raise PermissionDenied("Only admin or staff can review project requests.")

        try:
            project_request = ProjectRequest.objects.get(pk=pk)
        except ProjectRequest.DoesNotExist:
            raise NotFound("Project request not found.")

        new_status = request.data.get("status")
        delivery_date = request.data.get("delivery_date")

        if new_status not in ['pending', 'approved', 'rejected']:
            return Response({"error": "Invalid status value."}, status=status.HTTP_400_BAD_REQUEST)

        if delivery_date:
            project_request.delivery_date = delivery_date
            
        project_request.status = new_status
        project_request.reviewer = user
        project_request.review_date = timezone.now().date()  # Optionally update timestamp or add review_date

        project_request.save()

        serializer = ProjectUpdateResponseSerializer(project_request)
        return Response(serializer.data, status=status.HTTP_200_OK)