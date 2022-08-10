from django import forms

from shipping.models import ShippingAddress


class ShippingAddressForm(forms.ModelForm):

    class Meta:
        model = ShippingAddress
        fields = ('city', 'address', 'zipcode', 'number')

    def __init__(self, *args, **kwargs):
        super(ShippingAddressForm, self).__init__(*args, **kwargs)
        self.fields['city'].widget.attrs.update({'class': 'e-field-inner'})
        self.fields['address'].widget.attrs.update({'class': 'e-field-inner'})
        self.fields['zipcode'].widget.attrs.update({'class': 'e-field-inner'})
        self.fields['number'].widget.attrs.update({'class': 'e-field-inner'})







