from django.urls import path
from .views import PredictionList, PredictionDetail


urlpatterns = [
    path('predictions/', PredictionList.as_view(), name='prediction_list'),
    path('predictions/<int:pk>/', PredictionDetail.as_view(), name='prediction_detail'),
]
