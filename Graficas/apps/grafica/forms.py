from django import forms

class Upload(forms.Form):
    nombre= forms.CharField(max_length=50)