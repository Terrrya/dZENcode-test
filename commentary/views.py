from rest_framework import viewsets

from commentary.models import Commentary
from commentary.serializers import CommentarySerializer


class CommentaryViewSet(viewsets.ModelViewSet):
    serializer_class = CommentarySerializer
    queryset = Commentary.objects.all()
