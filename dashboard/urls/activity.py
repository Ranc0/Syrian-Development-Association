from django.urls import path
from dashboard.views import ActivityDashboardViewSet

urlpatterns = [
    path('activities/', ActivityDashboardViewSet.as_view({'get': 'list', 'post': 'create'}), name='activity-list-create'),
    path('activities/<int:pk>/', ActivityDashboardViewSet.as_view({'get': 'retrieve', 'delete': 'destroy' , "patch":"partial_update"}), name='activity-detail'),
]
