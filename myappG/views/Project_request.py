from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied, NotFound
from ..models import ProjectRequest, Beneficiary
from ..serializers import ProjectRequestSerializer

class ProjectRequestViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Disable list view
        return ProjectRequest.objects.none()

    def list(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def get_object(self):
        user = self.request.user

        if user.user_type == 'beneficiary':
            try:
                beneficiary = Beneficiary.objects.get(user=user)
                return ProjectRequest.objects.get(beneficiary=beneficiary)
            except (Beneficiary.DoesNotExist, ProjectRequest.DoesNotExist):
                raise NotFound("No project request found for this user.")
        else:
            return super().get_object()  # Allow staff/admin to access normally

    def retrieve(self, request, *args, **kwargs):
        obj = self.get_object()
        serializer = self.get_serializer(obj)
        return Response(serializer.data)

    def perform_create(self, serializer):
        user = self.request.user
        if user.user_type == 'beneficiary':
            try:
                beneficiary = Beneficiary.objects.get(user=user)
            except Beneficiary.DoesNotExist:
                raise PermissionDenied("You must be a registered beneficiary.")

            if ProjectRequest.objects.filter(beneficiary=beneficiary).exists():
                raise PermissionDenied("You have already submitted a project request.")

            serializer.save(beneficiary=beneficiary)
        else:
            serializer.save()

    def update(self, request, *args, **kwargs):
        raise PermissionDenied("Updating project requests is not allowed.")

    def partial_update(self, request, *args, **kwargs):
        raise PermissionDenied("Updating project requests is not allowed.")

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.status != 'pending':
            raise PermissionDenied("Only pending project requests can be deleted.")
        return super().destroy(request, *args, **kwargs)