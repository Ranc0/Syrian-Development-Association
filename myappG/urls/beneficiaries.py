from django.urls import path
from ..views import BeneficiaryViewSet

urlpatterns = [
    path('', BeneficiaryViewSet.as_view({'post': 'create'}), name='beneficiary-create'),
    path('me/', BeneficiaryViewSet.as_view({'get': 'me', 'patch': 'me'}), name='beneficiary-me'),
]