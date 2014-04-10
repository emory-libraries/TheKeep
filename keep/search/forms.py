from django import forms

from keep.repoadmin.forms import SolrSearchField

class SearchForm(forms.Form):
    'Public-facing search form, with keyword search'
    keyword = SolrSearchField(required=False,
        widget=forms.TextInput(attrs={'class':'form-control'}),
        help_text='One or more keywords; can include (but not start with) wildcards * and ?, and exact phrases in quotes.')
