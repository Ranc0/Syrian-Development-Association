from django.urls import path
from ..views import ProjectRequestViewSet

urlpatterns = [
    path('', ProjectRequestViewSet.as_view({'post': 'create'}), name='project-request-create'),

    path('me/', ProjectRequestViewSet.as_view({'get': 'retrieve'}), name='project-request-me'),

    path('me/delete/', ProjectRequestViewSet.as_view({'delete': 'destroy'}), name='project-request-delete'),
]