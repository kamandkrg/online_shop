from django import forms

from product.models import Product


class AddToBasketForm(forms.Form):
    product = forms.ModelChoiceField(queryset=Product.objects.all(),
                                     widget=forms.HiddenInput)
    quantity = forms.IntegerField(widget=forms.NumberInput(attrs={"class": "quantity"}))

    def save(self, basket):
        product = self.cleaned_data['product']
        quantity = self.cleaned_data['quantity']
        basket.add(product, quantity)
        return basket

