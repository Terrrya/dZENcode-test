from django.contrib.auth import get_user_model
from django.db import models


class Commentary(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="commentaries"
    )
    parent_commentary = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        related_name="child_commentaries",
        blank=True,
        null=True,
    )
    body = models.TextField()
