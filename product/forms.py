from django import forms

from lib.validations import rate_validate
from product.models import ProductRate


class ProductRateForm(forms.ModelForm):
    rate = forms.IntegerField(validators=[rate_validate], widget=forms.NumberInput(
        attrs={'type': "number", 'id': "quantity", 'name': "quantity", 'min': "0", 'max': "5"}))

    class Meta:
        model = ProductRate
        fields = ('rate', 'product')
