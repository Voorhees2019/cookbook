from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from versatileimagefield.fields import VersatileImageField


class Recipe(models.Model):
    """A model to represent a recipe."""

    title = models.CharField(verbose_name=_("Recipe title"), max_length=255)
    image = VersatileImageField(
        verbose_name=_("Recipe image"),
        blank=True,
        null=True,
        upload_to="recipe_images/",
    )
    description = models.TextField(verbose_name=_("Recipe description"))
    created_at = models.DateTimeField(verbose_name=_("Date created"), auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=_("Date updated"), auto_now=True)

    class Meta:
        ordering = ("title",)

    def get_absolute_url(self):
        return reverse("recipe-detail", kwargs={"pk": self.pk})

    def save(self, *args, **kwargs):
        """Delete the previous image from the storage if a new one has been uploaded."""

        try:
            recipe = Recipe.objects.get(pk=self.pk)
            if recipe.image != self.image:
                # Delete the image thumbnail and the actual image file
                recipe.image.thumbnail["100x100"].delete()
                recipe.image.delete(save=False)  # `save=False` to prevent a recursive save
        except:
            pass
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
