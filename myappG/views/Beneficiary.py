from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, NotFound, PermissionDenied
from rest_framework.decorators import action
from ..models import Beneficiary
from ..serializers import BeneficiarySerializer

class BeneficiaryViewSet(viewsets.ModelViewSet):
    queryset = Beneficiary.objects.all()
    serializer_class = BeneficiarySerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        return Beneficiary.objects.none()  

    def list(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def retrieve(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def perform_create(self, serializer):
        if Beneficiary.objects.filter(user=self.request.user).exists():
            raise ValidationError("This user already has a beneficiary.")
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get', 'patch'], url_path='me')
    def me(self, request):
        try:
            beneficiary = Beneficiary.objects.get(user=request.user)
        except Beneficiary.DoesNotExist:
            raise NotFound("No beneficiary profile found for this user.")

        if request.method == 'GET':
            serializer = self.get_serializer(beneficiary)
            return Response(serializer.data)

        if request.method == 'PATCH':
            serializer = self.get_serializer(beneficiary, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
