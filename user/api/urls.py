from . import views
from django.urls import path

urlpatterns = [
    path("login/", views.UserLoginAPIView.as_view(), name="login-api-view"),
    path("registration/", views.UserRegisterAPIView.as_view(), name="register-api-view"),
    path("profile/", views.UserProfileAPIView.as_view(), name="profile-api-view"),
    path("edit-profile/", views.UserEditProfileAPIView.as_view(), name="edit-profile-api-view"),
    path("deactivate-account/", views.deactivate_account, name="deactivate-account-api-view"),
    path("change-password/", views.ChangePasswordAPIView.as_view(), name="change-password"),
    path("get-content/", views.get_content_for_app, name="get-content")
]
