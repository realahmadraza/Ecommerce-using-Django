from django import forms
from .models import CartItem, UserAddress
class CartItemForm(forms.ModelForm):
    class Meta:
        model = CartItem
        fields = ['quantity']
        
class DeliveryAddressForm(forms.ModelForm):
    class Meta:
        model = UserAddress
        fields = ['name', 'phone', 'pin', 'locality', 'address', 'city', 'state', 'landmark', 'alternate_phone']