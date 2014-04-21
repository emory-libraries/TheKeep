from django import forms
from eultheme.forms import TelephoneInput

from keep.repoadmin.forms import SolrSearchField

class SearchForm(forms.Form):
    'Public-facing search form, with keyword search'
    keyword = SolrSearchField(required=False,
        widget=forms.TextInput(attrs={'class':'form-control'}),
        help_text='One or more keywords; can include (but not start with) wildcards * and ?, and exact phrases in quotes.')
    collection = forms.CharField(required=False,
        help_text='Search by collection number or words in collection name',
        widget=forms.TextInput(attrs={'placeholder':'Search by collection name or number',
                                      'class': 'form-control'}))

    start_date = forms.IntegerField(required=False,
        help_text=''''Search by start year;  use with end date to specify a range or single year''',
        widget=TelephoneInput(attrs={'class': 'form-control', 'placeholder': 'Start year'}))
    end_date = forms.IntegerField(required=False,
        help_text='Search by end date; use with start date to specify a range or single year',
        widget=TelephoneInput(attrs={'class': 'form-control', 'placeholder': 'End year'}))

    _adv_fields = ['collection']

    @property
    def advanced_fields(self):
        'list fields that are considered part of the "advanced" search'
        return [self[f] for f in self._adv_fields]
