from django.urls import path
from ..views import FeedbackView

urlpatterns = [
    path('add/',FeedbackView.as_view(),name='feedback'),
    path('get/',FeedbackView.as_view(),name='get-feedback'),
]