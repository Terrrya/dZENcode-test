from typing import Type

from django.core.cache import cache
from django.db.models import QuerySet
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import viewsets, mixins
from rest_framework.serializers import ModelSerializer

from commentary.models import Commentary
from commentary.permissions import IsAuthenticatedOrIfNonAuthenticatedReadOnly
from commentary.serializers import (
    CommentarySerializer,
    CreateCommentarySerializer,
    ListCommentarySerializer,
)


class CommentaryViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
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

        queryset = self.queryset.filter(
            parent_commentary=None
        ).prefetch_related("child_commentaries")

        if ordering in ("username", "email"):
            queryset = queryset.order_by(f"user__{ordering}")

        if ordering in ("-username", "-email"):
            queryset = queryset.order_by(f"-user__{ordering[1:]}")

        if ordering == "created_at":
            queryset = queryset.order_by(ordering)

        return queryset

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "ordering",
                type=OpenApiTypes.STR,
                description="Add ordering to commentaries. "
                "(ex. ?ordering=username). "
                "Can use username, email, created_at for ascending "
                "ordering or -username, -email for descending ordering. "
                "By default ordering is -created_at",
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
