from datetime import timedelta
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied
from django.utils import timezone
from datetime import timedelta

from myappG.models import (
    MedicalAidRequest,
    MaterialAidRequest,
    ProjectRequest
)


def get_period_filters(period: str):
    today = timezone.now().date()
    
    if period == "day":
        return {"request_date": today}
    elif period == "week":
        start = today - timedelta(days=today.weekday())
        return {"request_date__gte": start}
    elif period == "month":
        return {"request_date__year": today.year, "request_date__month": today.month}
    elif period == "year":
        return {"request_date__year": today.year}
    return {}  # 'all' or unknown

class MedicalAidStatsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        if request.user.user_type not in ['admin', 'staff']:
            raise PermissionDenied("You do not have permission to access this dashboard.")
        
        filters = get_period_filters(request.query_params.get('period', 'all').lower())
        qs = MedicalAidRequest.objects.filter(**filters)
        
        return Response({
            "total": qs.count(),
            "approved": qs.filter(status="approved").count(),
            "rejected": qs.filter(status="rejected").count()
        })

class MaterialAidStatsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        if request.user.user_type not in ['admin', 'staff']:
            raise PermissionDenied("You do not have permission to access this dashboard.")
        
        filters = get_period_filters(request.query_params.get('period', 'all').lower())
        qs = MaterialAidRequest.objects.filter(**filters)
        
        return Response({
            "total": qs.count(),
            "approved": qs.filter(status="approved").count(),
            "rejected": qs.filter(status="rejected").count()
        })

class AgriculturalProjectStatsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        if request.user.user_type not in ['admin', 'staff']:
            raise PermissionDenied("You do not have permission to access this dashboard.")
        
        filters = get_period_filters(request.query_params.get('period', 'all').lower())
        qs = ProjectRequest.objects.filter(project_type="agricultural", **filters)
        
        return Response({
            "total": qs.count(),
            "approved": qs.filter(status="approved").count(),
            "rejected": qs.filter(status="rejected").count()
        })

class CommercialProjectStatsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        if request.user.user_type not in ['admin', 'staff']:
            raise PermissionDenied("You do not have permission to access this dashboard.")
        
        filters = get_period_filters(request.query_params.get('period', 'all').lower())
        qs = ProjectRequest.objects.filter(project_type="commercial", **filters)
        
        return Response({
            "total": qs.count(),
            "approved": qs.filter(status="approved").count(),
            "rejected": qs.filter(status="rejected").count()
        })