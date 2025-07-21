from django.urls import path
from .views  import HomePageView, ErrorPage

core_patterns = ([
    path('', HomePageView.as_view(), name="inicio"),
    path('error',ErrorPage.as_view(), name = "error")
], "core")