from django.urls import path

from . import views

urlpatterns = [
    path("login", views.login_page, name="login"),
    path("login/submit", views.login_submit, name="login_submit"),
    path("logout", views.logout_submit, name="logout"),
    path("settings", views.settings_page, name="settings"),
    path("settings/profile", views.update_profile, name="settings_profile"),
    path("settings/email", views.update_email, name="settings_email"),
    path("settings/password", views.update_password, name="settings_password"),
    path("settings/users", views.create_user, name="settings_create_user"),
]
