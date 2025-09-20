from django.urls import path
from ..views import NewsViewSet

urlpatterns = [
    path('', NewsViewSet.as_view({'get': 'list'}), name='news-list'),
    path('<int:pk>/', NewsViewSet.as_view({'get': 'retrieve'}), name='news-detail'),
]