from django.urls import path
from ..views import ActivityViewSet

urlpatterns = [
    path('', ActivityViewSet.as_view({
        'get': 'list'
    }), name='activity-list'),

    path('<int:pk>/', ActivityViewSet.as_view({
        'get': 'retrieve'
    }), name='activity-detail'),
]