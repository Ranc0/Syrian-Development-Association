from django.urls import path
from dashboard.views import NewsDashboardViewSet

urlpatterns = [
    path('news/', NewsDashboardViewSet.as_view({'get': 'list', 'post': 'create'}), name='news-list-create'),
    path('news/<int:pk>/', NewsDashboardViewSet.as_view({'get': 'retrieve', 'delete': 'destroy' ,'patch':'partial_update'}), name='news-detail'),
]