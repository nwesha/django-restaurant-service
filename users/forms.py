from django import forms
from .models import CartItem, UserProfile

class CartItemForm(forms.ModelForm):
    class Meta:
        model = CartItem
        fields = ['quantity']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['full_name', 'birthday', 'address', 'gender', 'phone_number', 'email_id']
        widgets = {
            'birthday': forms.DateInput(attrs={'type': 'date'}),
            'gender': forms.Select(choices=UserProfile.GENDER_CHOICES),
        }