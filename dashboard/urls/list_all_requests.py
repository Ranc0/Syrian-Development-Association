from django.urls import path
from dashboard.views import AllAidAndProjectRequestsView

urlpatterns = [
   path('requests/all/', AllAidAndProjectRequestsView.as_view(), name='all-requests-list'),

]
