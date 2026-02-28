from django.urls import path
from .views import exam_page

urlpatterns = [
    path("", exam_page, name="exam"),
]