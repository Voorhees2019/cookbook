from django.db.models.signals import pre_delete
from django.dispatch import receiver

from apps.recipes.models import Recipe


@receiver(pre_delete, sender=Recipe)
def delete_recipe_image(sender, instance, **kwargs):
    """
    Must delete recipe images from storage here but not in model's `delete()` method because
    delete() method for an object is not necessarily called when deleting objects in bulk
    using a QuerySet.
    """
    instance.image.delete()
