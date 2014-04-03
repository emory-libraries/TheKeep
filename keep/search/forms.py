from django import forms

class SearchForm(forms.Form):
    'Public-facing search form, with keyword search'
    keyword = forms.CharField(required=False,
        widget=forms.TextInput(attrs={'class':'form-control'}),
        help_text='One or more keywords; can include wildcards * and ?, and exact phrases in quotes.')
