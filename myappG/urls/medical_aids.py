from django.urls import path
from ..views import MedicalAidRequestViewSet

urlpatterns = [
    path('', MedicalAidRequestViewSet.as_view({'post': 'create'}), name='medical-aid-create'),

    path('me/', MedicalAidRequestViewSet.as_view({'get': 'retrieve'}), name='medical-aid-me'),

    path('me/delete/', MedicalAidRequestViewSet.as_view({'delete': 'destroy'}), name='medical-aid-delete'),
]