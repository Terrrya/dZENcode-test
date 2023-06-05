from rest_framework import serializers

from commentary.models import Commentary


class CommentarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Commentary
        fields = ("id", "created_at", "user", "parent_commentary", "body")


class CreateCommentarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Commentary
        fields = ("id", "parent_commentary", "body")
