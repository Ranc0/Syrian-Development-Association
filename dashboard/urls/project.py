from django.urls import path
from dashboard.views import (
    ProjectRequestDashboardListView,
    ProjectRequestDashboardDetailView,
    ProjectReviewStatusUpdateView
)

urlpatterns = [
    path('projects/', ProjectRequestDashboardListView.as_view(), name='project-request-list'),
    path('projects/<int:pk>/', ProjectRequestDashboardDetailView.as_view(), name='project-request-detail'),
    path('projects/<int:pk>/review/', ProjectReviewStatusUpdateView.as_view(), name='project-review'),
]