from django.urls import path
from . import views


urlpatterns = [
    path("ad/<int:ad_pk>/", views.AdCommentCreateView.as_view(), name="comment-list-create"),
    path("contractor/<int:contractor_pk>/", views.ContractorCommentsListView.as_view(), name="contractor-comments-list"),
]
