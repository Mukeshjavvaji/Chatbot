from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index),
    path('<int:ck>', views.display),
    path('<int:ck>/send', views.send, name='send-message'),
    path('newconvo', views.newconvo)
]