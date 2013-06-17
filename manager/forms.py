from django import forms

class FitForm(forms.Form):
    fit = forms.CharField()
    description = forms.CharField()