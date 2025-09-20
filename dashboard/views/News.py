from rest_framework import viewsets, permissions, status
from rest_framework.exceptions import PermissionDenied
from myappG.models import News
from dashboard.serializers import NewsSerializer  

class NewsDashboardViewSet(viewsets.ModelViewSet):
    serializer_class = NewsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.user_type not in ['admin', 'staff']:
            raise PermissionDenied("Access restricted to admin/staff users.")
        return News.objects.all()

    def destroy(self, request, *args, **kwargs):
        if request.user.user_type not in ['admin', 'staff']:
            raise PermissionDenied("Only admin/staff can delete news entries.")
        return super().destroy(request, *args, **kwargs)