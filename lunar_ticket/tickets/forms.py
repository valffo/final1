from django import forms

class OrderForm(forms.Form):
    ticket = forms.CharField()
    DATE_INPUT_FORMATS = 'd.m.Y'
    date_purchase = forms.DateField()
