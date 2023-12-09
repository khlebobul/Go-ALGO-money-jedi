from django.urls import path

from . import views

from django.urls import path
from . import views
from django.conf import settings

urlpatterns = [
    path('api/news/<str:ticker>', views.getNews),
]