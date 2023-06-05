from rest_framework import serializers

from commentary.models import Commentary


class CommentarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Commentary
        fields = (
            "id",
            "user",
            "parent_commentary",
            "body",
        )
