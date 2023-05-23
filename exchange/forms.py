from django import forms


class CalculationForm(forms.Form):
    num = forms.FloatField(label="", min_value=0)
