from django.urls import path
from ..views import MaterialAidRequestViewSet

urlpatterns = [
    path('', MaterialAidRequestViewSet.as_view({'post': 'create'}), name='material-aid-create'),

    path('me/', MaterialAidRequestViewSet.as_view({'get': 'retrieve'}), name='material-aid-me'),

    path('me/delete/', MaterialAidRequestViewSet.as_view({'delete': 'destroy'}), name='material-aid-delete'),
]