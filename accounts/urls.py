from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path("login/", views.LoginView.as_view(), name="login"),
    path("token/refresh/", views.RefreshView.as_view(), name="token_refresh"),
    path("register/", views.UserRegisterView.as_view(), name="user_register"),
    path("profile/<int:pk>/", views.UserProfileDetailView.as_view(), name="user_profile_detail"),
    path("contractors/", views.ContractorListView.as_view(), name="contractor_list"),
]
