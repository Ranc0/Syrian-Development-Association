from rest_framework import viewsets, permissions, status
from rest_framework.exceptions import PermissionDenied
from myappG.models import Activity
from dashboard.serializers import ActivitySerializer  

class ActivityDashboardViewSet(viewsets.ModelViewSet):
    serializer_class = ActivitySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.user_type not in ['admin', 'staff']:
            raise PermissionDenied("Access restricted to admin/staff users.")
        return Activity.objects.all()

    def destroy(self, request, *args, **kwargs):
        user = request.user
        if user.user_type not in ['admin', 'staff']:
            raise PermissionDenied("Only admin/staff can delete activities.")
        return super().destroy(request, *args, **kwargs)