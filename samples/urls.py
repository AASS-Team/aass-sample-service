from django.urls import path

from . import views

urlpatterns = [
    path("", views.SamplesList.as_view()),
    path("<uuid:id>", views.SampleDetail.as_view()),
    path("bulk", views.BulkSamplesList.as_view()),
]
