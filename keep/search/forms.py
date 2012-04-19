from django import forms

class KeywordSearch(forms.Form):
    keyword = forms.CharField(required=True)
