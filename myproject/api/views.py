from rest_framework import generics
from rest_framework.response import Response
from .models import Prediction
from .serializers import PredictionSerializer


class PredictionList(generics.ListCreateAPIView):
    queryset = Prediction.objects.all()
    serializer_class = PredictionSerializer



class PredictionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Prediction.objects.all()
    serializer_class = PredictionSerializer
