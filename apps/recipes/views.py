from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView, View

from apps.recipes.models import Recipe


def index(request):
    return render(request, "index.html", {})


class RecipeListView(ListView):
    """LIST view for the recipe model."""

    model = Recipe
    template_name = "recipes/recipes.html"
    context_object_name = "recipes"
    ordering = ("-created_at",)
    paginate_by = settings.PAGE_SIZE


class BaseRecipeView(LoginRequiredMixin, UserPassesTestMixin, View):
    """Basic view for creating and updating a recipe."""

    model = Recipe
    fields = ("title", "image", "description")
    success_url = reverse_lazy("recipes")
    template_name = "recipes/recipe_create.html"

    def test_func(self):
        """Ensure only admin can create or update a recipe."""
        return self.request.user.is_superuser


class RecipeCreateView(BaseRecipeView, CreateView):
    """CREATE view for the recipe model."""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["viewtype"] = "create"
        return context


class RecipeDetailView(DetailView):
    """DETAIL view for the recipe model."""

    model = Recipe
    template_name = "recipes/recipe_detail.html"
    context_object_name = "recipe"


class RecipeUpdateView(BaseRecipeView, UpdateView):
    """UPDATE view for the recipe model."""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["viewtype"] = "update"
        return context


class RecipeDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """DELETE view for the recipe model."""

    model = Recipe
    success_url = reverse_lazy("recipes")

    def test_func(self):
        """Ensure only admin can delete a recipe."""
        return self.request.user.is_superuser
