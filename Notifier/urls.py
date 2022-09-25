from django.urls import path, include
from django.conf import settings
from . import views
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", views.index, name="home"),
    path("login/", views.login, name="login"),
    path("get_notification/", views.get_notification, name="get_notification"),
    path("set_notification/", views.setNotification, name="setNotification"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("social-auth/", include("social_django.urls"), name="social"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# add MyContest to Contest automatically when creating Contest
# add new_contest to Platform whenever new contests added