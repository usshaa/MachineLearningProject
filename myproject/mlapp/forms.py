from django import forms

class PredictionForm(forms.Form):
    product = forms.IntegerField()
    quantity = forms.IntegerField()
    price = forms.FloatField()
    month = forms.IntegerField()
    city = forms.CharField()
    hour = forms.IntegerField()
