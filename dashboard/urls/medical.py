from django.urls import path
from ..views import MedicalAidDashboardView ,MedicalAidRequestDetailDashboardView , MedicalAidReviewStatusUpdateView

urlpatterns = [
    path('medical/', MedicalAidDashboardView.as_view(), name='dashboard-medical-list'),
    path('medical/<int:pk>/', MedicalAidRequestDetailDashboardView.as_view(), name='dashboard-medical-detail'),
    path('medical/<int:pk>/review/', MedicalAidReviewStatusUpdateView.as_view(), name='dashboard-medical-review'),
]
