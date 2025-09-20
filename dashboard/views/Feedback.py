from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from rest_framework.exceptions import PermissionDenied
from itertools import chain
from operator import attrgetter
from myappG.models import Feedback

from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Avg
from myappG.models import Feedback  

class DashboardFeedbackView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.user_type not in ['admin', 'staff']:
            raise PermissionDenied("فقط مسؤولو وموظفو الجمعية يمكنهم الوصول إلى هذه البيانات")

        total = Feedback.objects.count()
        avg_rating = Feedback.objects.aggregate(avg=Avg('rating'))['avg'] or 0
        satisfied_yes = Feedback.objects.filter(is_satisfied=True).count()
        satisfied_no = Feedback.objects.filter(is_satisfied=False).count()
        reuse_yes = Feedback.objects.filter(will_use_again=True).count()
        reuse_no = Feedback.objects.filter(will_use_again=False).count()
        notes_list = Feedback.objects.exclude(notes__isnull=True).exclude(notes__exact='').values_list('notes', flat=True)

        return Response({
            "total_feedbacks": total,
            "average_rating": round(avg_rating, 2),
            "is_satisfied": {
                "yes": satisfied_yes,
                "no": satisfied_no,
            },
            "will_use_again": {
                "yes": reuse_yes,
                "no": reuse_no,
            },
             "notes": list(notes_list)
        })