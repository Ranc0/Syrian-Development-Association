from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from rest_framework.exceptions import PermissionDenied
from itertools import chain
from operator import attrgetter

from myappG.models import MedicalAidRequest, MaterialAidRequest, ProjectRequest
from dashboard.serializers import DashboardBeneficiarySerializer

class AllAidAndProjectRequestsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        if request.user.user_type not in ['admin', 'staff']:
            raise PermissionDenied("Access is restricted to admin or staff users.")

        medical_qs = MedicalAidRequest.objects.select_related('beneficiary', 'reviewer')
        material_qs = MaterialAidRequest.objects.select_related('beneficiary', 'reviewer')
        project_qs = ProjectRequest.objects.select_related('beneficiary', 'reviewer')

        combined = sorted(
            chain(medical_qs, material_qs, project_qs),
            key=attrgetter('request_date'),
            reverse=True
        )

        serialized = []
        for obj in combined:
            if isinstance(obj, MedicalAidRequest):
                category = "مساعدة طبية"
                aid_display = "مساعدة طبية"
            elif isinstance(obj, MaterialAidRequest):
                category = "مساعدة مادية"
                aid_display = "مساعدة مادية"
            elif isinstance(obj, ProjectRequest):
                category = "مشروع"
                aid_display = obj.get_project_type_display()
            else:
                continue  # safety net

            serialized.append({
                "id" : obj.id ,
                "category": category,
                "status_display": obj.get_status_display(),
                "aid_type_display": aid_display,
                "request_date": obj.request_date,
                "reviewer": obj.reviewer.get_full_name() if obj.reviewer else "",
                "beneficiary": DashboardBeneficiarySerializer(obj.beneficiary).data
            })

        return Response(serialized, status=status.HTTP_200_OK)