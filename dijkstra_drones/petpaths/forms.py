from django import forms

class PointForm(forms.Form):
    latitude = forms.FloatField()
    longitude = forms.FloatField()