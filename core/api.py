from document.serializers import DocumentSerializer
from django.utils.timezone import now, timedelta
from rest_framework.response import Response
from rest_framework.views import APIView
from document.models import Document


class DashboardAPIView(APIView):
    def get(self, request):
        user = request.user
        last_month = now() - timedelta(days=30)

        # Last 5 documents
        last_five_documents = Document.objects.filter(user=user).order_by(
            "-created_at"
        )[:5]
        last_five_documents_serialized = DocumentSerializer(
            last_five_documents, many=True
        ).data

        # Total documents count
        total_documents = Document.objects.filter(user=user).count()

        # Documents added in the last month
        last_month_documents = Document.objects.filter(
            user=user, created_at__gte=last_month
        ).count()

        # Pending documents count
        pending_documents = Document.objects.filter(
            user=user, status=Document.ProcessingStatus.PENDING
        ).count()

        # Total storage used
        storage_used = sum(doc.size for doc in Document.objects.filter(user=user))

        return Response(
            {
                "last_five_documents": last_five_documents_serialized,
                "total_documents": total_documents,
                "last_month_documents": last_month_documents,
                "pending_documents": pending_documents,
                "storage_used": storage_used,
            }
        )
