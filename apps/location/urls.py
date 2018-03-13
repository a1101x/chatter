from django.urls import path

from apps.location.views import LocationDetailView, LocationListView

app_name = 'reward'
urlpatterns = [
    path('list/', LocationListView.as_view()),
    path('detail/<int:pk>/', LocationDetailView.as_view()),
]
