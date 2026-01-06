from django.urls import path
from . import views


urlpatterns = [
    path("<int:ad_pk>/comment/", views.AdCommentCreateView.as_view(), name="comment-list-create"),
]
