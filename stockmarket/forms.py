from django import forms
from .models import CustomUser,Stock
from django.contrib.auth.forms import AuthenticationForm

# class LoginForm(AuthenticationForm):
#     username = forms.CharField(label="Username", max_length=30,
#                                widget=forms.TextInput(attrs={'name': 'username'}))
#     password = forms.CharField(label="Password", max_length=30,
#                                widget=forms.TextInput(attrs={'name': 'password'}))
from dal import autocomplete

class StockForm(forms.ModelForm):
    name = forms.ModelChoiceField(
        queryset=Stock.objects.all(),
        widget=autocomplete.ModelSelect2(url='stock-auto')
    )

    class Meta:
        model = Stock
        fields = ('name', )