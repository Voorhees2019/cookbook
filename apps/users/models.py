from django.db import models
from django.utils.translation import gettext_lazy as _


class GenderChoices(models.TextChoices):
    """Class to define a user's gender."""

    MALE = "M", _("Male")
    FEMALE = "F", _("Female")
    OTHER = "O", _("Other")


class Profile(models.Model):
    """A model to represent a telegram user."""

    external_id = models.PositiveIntegerField(verbose_name=_("User ID in Telegram"), unique=True)
    name = models.CharField(verbose_name=_("Name of a user"), max_length=255)
    gender = models.CharField(
        verbose_name=_("Gender"),
        max_length=1,
        choices=GenderChoices.choices,
        default=GenderChoices.OTHER,
    )
    username = models.CharField(
        verbose_name=_("Telegram Username"),
        max_length=32,
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(verbose_name=_("Date created"), auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=_("Date updated"), auto_now=True)

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return self.name
