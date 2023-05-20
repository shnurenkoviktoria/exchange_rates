from django import forms


class CalculationForm(forms.Form):
    num = forms.FloatField(min_value=0)
