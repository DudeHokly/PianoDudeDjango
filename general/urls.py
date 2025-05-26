from django.urls import path
from .views import (
    index,
    logout_view,
    register,
    panel_admin,
    account,
    contacts,
    login_view,
    feedback,
    admin_user_list,
    panel_admin_Users,
)

app_name = "general"

urlpatterns = [
    path("", index, name="index"),
    path("logout/", logout_view, name="logout"),
    path("accounts/login/", login_view, name="login"),
    path("register/", register, name="register"),
    path("panel_admin/", panel_admin, name="panel_admin"),
    path("account/", account, name="account"),
    path("contacts/", contacts, name="contacts"),
    path("feedback/", feedback, name="feedback"),
    path("users/", admin_user_list, name="user_list"),
    path("users/<int:user_id>/edit/", panel_admin_Users, name="user_edit"),
]
