# myappG/urls/evaluations.py
from django.urls import path
from ..views import EvaluationViewSet

urlpatterns = [
    path('', EvaluationViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }), name='evaluation-list'),
    
    path('<int:pk>/', EvaluationViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update'
    }), name='evaluation-detail'),
    
    path('beneficiary/<int:beneficiary_id>/', EvaluationViewSet.as_view({
        'get': 'by_beneficiary'
    }), name='evaluation-by-beneficiary'),
    
    path('<int:pk>/approve/', EvaluationViewSet.as_view({
        'post': 'approve_evaluation'
    }), name='evaluation-approve'),
    
    path('stats/', EvaluationViewSet.as_view({
        'get': 'evaluation_stats'
    }), name='evaluation-stats'),
]