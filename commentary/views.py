from typing import Type

from rest_framework import viewsets
from rest_framework.serializers import ModelSerializer

from commentary.models import Commentary
from commentary.permissions import IsAuthenticatedOrIfNonAuthenticatedReadOnly
from commentary.serializers import (
    CommentarySerializer,
    CreateCommentarySerializer,
)


class CommentaryViewSet(viewsets.ModelViewSet):
    queryset = Commentary.objects.all()
    permission_classes = (IsAuthenticatedOrIfNonAuthenticatedReadOnly,)

    def get_serializer_class(self, *args, **kwargs) -> Type[ModelSerializer]:
        if self.action == "create":
            return CreateCommentarySerializer
        return CommentarySerializer

    def perform_create(self, serializer: CreateCommentarySerializer) -> None:
        serializer.save(user=self.request.user)
