from . import views
from django.urls import path


urlpatterns = [
    path("login/", views.UserLoginAPIView.as_view(), name="login-api-view"),
]
