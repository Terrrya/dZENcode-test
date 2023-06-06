from typing import Type

from django.core.cache import cache
from django.db.models import QuerySet
from rest_framework import viewsets
from rest_framework.serializers import ModelSerializer

from commentary.models import Commentary
from commentary.permissions import IsAuthenticatedOrIfNonAuthenticatedReadOnly
from commentary.serializers import (
    CommentarySerializer,
    CreateCommentarySerializer,
    ListCommentarySerializer,
)


class CommentaryViewSet(viewsets.ModelViewSet):
    queryset = Commentary.objects.all()
    permission_classes = (IsAuthenticatedOrIfNonAuthenticatedReadOnly,)

    def get_serializer_class(self, *args, **kwargs) -> Type[ModelSerializer]:
        if self.action == "create":
            return CreateCommentarySerializer
        if self.action == "list":
            return ListCommentarySerializer
        return CommentarySerializer

    def perform_create(self, serializer: CreateCommentarySerializer) -> None:
        cache.clear()
        serializer.save(user=self.request.user)

    def get_queryset(self) -> QuerySet:
        ordering = self.request.query_params.get("ordering")

        queryset = self.queryset.filter(parent_commentary=None)

        if ordering in ("username", "email"):
            queryset = queryset.order_by(f"user__{ordering}")

        if ordering in ("-username", "-email"):
            queryset = queryset.order_by(f"-user__{ordering[1:]}")

        if ordering == "created_at":
            queryset = queryset.order_by(ordering)

        return queryset
