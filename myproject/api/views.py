# views.py
import pickle
import pandas as pd
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import PredictionSerializer


class PredictionAPIView(APIView):

    def post(self, request, format=None):
        serializer = PredictionSerializer(data=request.data)
        if serializer.is_valid():
            # Load the saved model
            model = pickle.load(open('finalized_model.sav', 'rb'))

            # Get the form data
            product = serializer.validated_data['product']
            quantity = serializer.validated_data['quantity']
            price = serializer.validated_data['price']
            month = serializer.validated_data['month']
            city = serializer.validated_data['city']
            hour = serializer.validated_data['hour']

            # Create a DataFrame with the input data
            data = pd.DataFrame({'Product': [product], 'Quantity Ordered': [quantity], 'Price Each': [price],
                                 'Month': [month], 'City': [city], 'Hour': [hour]})

            # Convert categorical variables to numerical using one-hot encoding
            data = pd.get_dummies(data, columns=['Product','City'])

            # Load the column names used during training
            with open('columns.pkl', 'rb') as f:
                columns = pickle.load(f)

            # Ensure input data has same columns as during training
            missing_cols = set(columns) - set(data.columns)
            for c in missing_cols:
                data[c] = 0
            data = data[columns]

            # Make prediction
            prediction = model.predict(data)[0]

            # Return prediction in response
            return Response({'prediction': prediction}, status=status.HTTP_200_OK)

        # Return errors in response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
