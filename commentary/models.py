import os
import pathlib
import uuid

from PIL import Image
from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils.text import slugify
from rest_framework.exceptions import ValidationError


def upload_file_path(instance, filename):
    _, extension = os.path.splitext(filename)
    filename = f"{slugify(instance.id)}-{uuid.uuid4()}{extension}"

    return os.path.join("uploads/", filename)


class Commentary(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        to=get_user_model(),
        on_delete=models.CASCADE,
        related_name="commentaries",
    )
    parent_commentary = models.ForeignKey(
        to="self",
        on_delete=models.CASCADE,
        related_name="child_commentaries",
        blank=True,
        null=True,
    )
    body = models.TextField()
    uploads = models.FileField(
        upload_to=upload_file_path,
        null=True,
        validators=[
            FileExtensionValidator(
                allowed_extensions=["jpg", "png", "gif", "txt"]
            )
        ],
    )

    class Meta:
        verbose_name_plural = "Commentaries"
        ordering = ["-created_at"]

    def save(
        self,
        force_insert=False,
        force_update=False,
        using=None,
        update_fields=None,
    ):
        super().save(force_insert, force_update, using, update_fields)
        if self.uploads:
            file_ext = pathlib.Path(self.uploads.path).suffix

            if file_ext in (".jpg", ".png", ".gif"):
                with Image.open(self.uploads) as image:
                    if image.width > 320 or image.height > 240:
                        image.thumbnail((320, 240))
                        image.save(self.uploads.path)

            if file_ext == ".txt" and self.uploads.size > 100 * 1024:
                raise ValidationError(
                    {"uploads": "size of text file should be lower than 100KB"}
                )
