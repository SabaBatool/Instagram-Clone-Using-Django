from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Profile Section
    # path("profile/edit", EditProfile, name="editprofile"),
    # User Authentication
    path("sign-up/", views.register, name="polls/sign-up"),
    path(
        "sign-in/",
        auth_views.LoginView.as_view(
            template_name="polls/sign-in.html", redirect_authenticated_user=True
        ),
        name="sign-in",
    ),
    path(
        "sign-out/",
        auth_views.LogoutView.as_view(template_name="polls/sign-out.html"),
        name="sign-out",
    ),
]
