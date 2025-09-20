
from django.http import FileResponse, Http404
from django.conf import settings
import os
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny  # or IsAuthenticated if needed

@api_view(['GET'])
@permission_classes([AllowAny])  # Or restrict access if needed
def serve_media_file(request, path):
    full_path = os.path.join(settings.MEDIA_ROOT, path)
    if not os.path.exists(full_path):
        raise Http404("File not found.")
    
    # Infer content type from extension (optional)
    ext = os.path.splitext(path)[1].lower()
    content_type = {
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.png': 'image/png',
        '.webp': 'image/webp',
        '.pdf': 'application/pdf',
    }.get(ext, 'application/octet-stream')

    response = FileResponse(open(full_path, 'rb'), content_type=content_type)
    response['Access-Control-Allow-Origin'] = '*'
    return response
