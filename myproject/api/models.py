from django.db import models


class Prediction(models.Model):
    product = models.CharField(max_length=255)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    month = models.IntegerField()
    city = models.CharField(max_length=255)
    hour = models.IntegerField()
    prediction = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.product
