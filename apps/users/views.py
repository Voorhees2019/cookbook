from django.conf import settings
from django.views.generic import ListView

from apps.users.models import Profile


class ProfileListView(ListView):
    """LIST view for the Profile model."""

    model = Profile
    template_name = "profiles/profiles.html"
    context_object_name = "profiles"
    ordering = ("-created_at",)
    paginate_by = settings.PAGE_SIZE
