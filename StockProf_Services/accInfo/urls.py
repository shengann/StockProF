from django.urls import path

from accInfo import views

urlpatterns = [
    path('save-result', views.saveResult),
]
