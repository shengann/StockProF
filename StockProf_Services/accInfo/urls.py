from django.urls import path

from accInfo import views

urlpatterns = [
    path('save-result', views.saveResult),
    path('history', views.historyList.as_view()),
    path('history/<str:id>', views.historyDetails.as_view()),
]
