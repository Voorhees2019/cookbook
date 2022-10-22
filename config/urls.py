from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import include, path

from apps.recipes.views import index

urlpatterns = [
    path("", index, name="index"),
    path("recipes/", include("apps.recipes.urls")),
    path("users/", include("apps.users.urls")),
    # AUTH
    path(
        "login/",
        LoginView.as_view(template_name="auth/login.html", redirect_authenticated_user=True),
        name="login",
    ),
    path("logout/", LogoutView.as_view(), name="logout"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
