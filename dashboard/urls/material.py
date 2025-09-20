from django.urls import path
from ..views import MaterialAidDashboardListView , MaterialAidDashboardDetailView , MaterialAidReviewStatusUpdateView

urlpatterns = [
    path('material-aid/', MaterialAidDashboardListView.as_view(), name='material-aid-list'),
    path('material-aid/<int:pk>/', MaterialAidDashboardDetailView.as_view(), name='material-aid-detail'),
    path('material-aid/<int:pk>/review/', MaterialAidReviewStatusUpdateView.as_view(), name='material-aid-review'),
]