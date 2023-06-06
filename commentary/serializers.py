import re

from bs4 import BeautifulSoup
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from commentary.models import Commentary


class CommentarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Commentary
        fields = ("id", "created_at", "user", "parent_commentary", "body")


class ListCommentarySerializer(CommentarySerializer):
    class Meta:
        model = Commentary
        fields = ("id", "created_at", "user", "child_commentaries", "body")

    def get_fields(self):
        fields = super(ListCommentarySerializer, self).get_fields()
        fields["child_commentaries"] = ListCommentarySerializer(many=True)
        return fields


class CreateCommentarySerializer(CommentarySerializer):
    created_at = serializers.DateTimeField(read_only=True)
    user = serializers.SlugRelatedField(
        slug_field="id", read_only=True, many=False
    )

    def validate(self, attrs: dict) -> dict:
        data = super().validate(attrs)
        commentary_text = data["body"]

        if re.search(r"<(?!\/?(?:strong|i|code|a))[^>]*>", commentary_text):
            raise ValidationError(
                {
                    "body": "you should use only <strong>, <i>, <code>, "
                    "<a> tags"
                }
            )

        soup = BeautifulSoup(commentary_text, "html.parser")
        if str(soup) != commentary_text:
            raise ValidationError({"body": "You should use only html style"})

        return data
