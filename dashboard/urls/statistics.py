from django.urls import path
from dashboard.views import (
   MedicalAidStatsView , MaterialAidStatsView , AgriculturalProjectStatsView , CommercialProjectStatsView , DashboardFeedbackView
)

urlpatterns = [
    path('stats/medical/', MedicalAidStatsView.as_view(), name='stats-medical'),
    path('stats/material/', MaterialAidStatsView.as_view(), name='stats-material'),
    path('stats/projects/agricultural/', AgriculturalProjectStatsView.as_view(), name='stats-agricultural-projects'),
    path('stats/projects/commercial/', CommercialProjectStatsView.as_view(), name='stats-commercial-projects'),
    path('feedback/', DashboardFeedbackView.as_view(), name='stats-feedback'),
]

