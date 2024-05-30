from django.urls import path
from . import views

urlpatterns = [
    path('', views.make_traffic, name='make_traffic'),
]
