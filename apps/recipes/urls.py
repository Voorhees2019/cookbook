from django.urls import path

from apps.recipes import views

urlpatterns = [
    path("", views.RecipeListView.as_view(), name="recipes"),
    path("new/", views.RecipeCreateView.as_view(), name="recipe-create"),
    path("<int:pk>/", views.RecipeDetailView.as_view(), name="recipe-detail"),
    path("<int:pk>/update/", views.RecipeUpdateView.as_view(), name="recipe-update"),
    path("<int:pk>/delete/", views.RecipeDeleteView.as_view(), name="recipe-delete"),
]
