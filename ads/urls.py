from django.urls import path
from . import views


urlpatterns = [
    path("", views.AdListCreateView.as_view(), name="ad-list-create"),
    path("<int:pk>/", views.AdDetailView.as_view(), name="ad-detail"),
    path("<int:pk>/apply/", views.AdApplyView.as_view(), name="ad-apply"),
    path("<int:pk>/assign/", views.AdAssignProviderView.as_view(), name="ad-assign"),
    path("<int:pk>/complete/", views.AdProvideFinishView.as_view(), name="ad-complete"),
    path("<int:pk>/confirm/", views.AdOwnerConfirmView.as_view(), name="ad-confirm"),
]   