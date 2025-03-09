from document.serializers import DocumentSerializer
from django.utils.timezone import now, timedelta
from rest_framework.response import Response
from rest_framework.views import APIView
from document.models import Document


class DashboardAPIView(APIView):
    def get(self, request):
        user = request.user

        # Last 3 documents
        last_five_documents = Document.objects.filter(user=user).order_by(
            "-created_at"
        )[:3]
        last_five_documents_serialized = DocumentSerializer(
            last_five_documents, many=True
        ).data

        # Total documents count
        total_documents = Document.objects.filter(user=user).count()
    
        return Response(
            {
                "last_three_documents": last_five_documents_serialized,
                "total_documents": total_documents,
            }
        )
