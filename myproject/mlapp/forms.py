from django import forms

class PredictionForm(forms.Form):
    product = forms.IntegerField(required=False)
    quantity = forms.IntegerField()
    price = forms.FloatField()
    month = forms.IntegerField(required=False)
    city = forms.CharField(required=False)
    hour = forms.IntegerField(required=False)

    def clean_city(self):
        """Ignore empty city field if it is optional."""
        if self.cleaned_data['city'] == '':
            if self.fields['city'].required:
                raise forms.ValidationError("This field is required.")
            else:
                return None
        else:
            return self.cleaned_data['city']

    def clean_product(self):
        """Ignore empty product field if it is optional."""
        if self.cleaned_data['product'] == '':
            if self.fields['product'].required:
                raise forms.ValidationError("This field is required.")
            else:
                return None
        else:
            return self.cleaned_data['product']

