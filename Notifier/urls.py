from django.urls import path, include
from django.conf import settings
from . import views
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", views.home, name="home"),
    path("about_us/", views.aboutUs, name="aboutUs"),
    path("contact_us/", views.contactUs, name="contactUs"),
    path("contests/", views.contests, name="contests"),
    path("fetch_data/", views.scrape, name="scrape"),
    path("sign_up/", views.signUp, name="signUp"),
    path("login/", views.loginPage, name="login"),
    path("my_contest/", views.myContest, name="myContest"),
    path("set_notification/", views.setNotification, name="setNotification"),
    path("set_notification/add/<str:platform>", views.add, name="add"),
    path("set_notification/remove/<str:platform>", views.remove, name="remove"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("social-auth/", include("social_django.urls"), name="social"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# add MyContest to Contest automatically when creating Contest
# add new_contest to Platform whenever new contests added
