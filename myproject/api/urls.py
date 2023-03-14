from django.urls import path
from .views import PredictionAPIView

urlpatterns = [
    path('api_predict/', PredictionAPIView.as_view(), name='api_predict'),
]
